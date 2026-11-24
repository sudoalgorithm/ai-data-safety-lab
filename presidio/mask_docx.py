# /// script
# requires-python = ">=3.10,<3.13"
# dependencies = [
#   "presidio-analyzer",
#   "presidio-anonymizer",
#   "python-docx",
#   "rich",
#   "en_core_web_lg @ https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.8.0/en_core_web_lg-3.8.0-py3-none-any.whl",
# ]
# ///
"""Mask personal data inside a Word document, keeping its layout.

Usage:
    uv run presidio/mask_docx.py REPORT.docx [--outdir DIR] [--threshold 0.4]

Writes two files next to each other:
    REPORT.found.docx    the original, with everything Presidio detected highlighted in red
                         (anything NOT highlighted was missed: read it)
    REPORT.masked.docx   the same document with each finding replaced by a label such as <PERSON>

Uses the GCC recognisers and threshold from presidio/gcc_presidio.py. Runs locally; nothing is sent anywhere.
Covers body paragraphs, tables, headers and footers. Text inside images is not read.
"""

import argparse
import collections
import copy
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from docx import Document  # noqa: E402
from docx.enum.text import WD_COLOR_INDEX  # noqa: E402
from docx.shared import RGBColor  # noqa: E402
from gcc_presidio import build_analyzer, find_pii, load_deny  # noqa: E402
from presidio_anonymizer import AnonymizerEngine  # noqa: E402
from presidio_anonymizer.entities import OperatorConfig  # noqa: E402
from rich.console import Console  # noqa: E402
from rich.table import Table  # noqa: E402


def paragraphs(doc):
    """Every paragraph in the body, tables (including nested), headers and footers."""
    def walk(container):
        for p in container.paragraphs:
            yield p
        for t in getattr(container, "tables", []):
            for row in t.rows:
                for cell in row.cells:
                    yield from walk(cell)
    yield from walk(doc)
    for s in doc.sections:
        for part in (s.header, s.footer):
            yield from walk(part)


def rewrite(p, pieces):
    """Replace a paragraph's runs with `pieces` [(text, style)], keeping the first run's formatting."""
    if not p.runs:
        return
    proto = copy.deepcopy(p.runs[0]._r)
    for r in list(p.runs):
        r._r.getparent().remove(r._r)
    for text, style in pieces:
        r_el = copy.deepcopy(proto)
        for t in r_el.findall("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t"):
            r_el.remove(t)
        p._p.append(r_el)
        run = p.runs[-1]
        run.text = text
        if style == "found":
            run.font.highlight_color = WD_COLOR_INDEX.RED
            run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
            run.bold = True
        elif style == "label":
            run.font.highlight_color = WD_COLOR_INDEX.YELLOW
            run.bold = True


def dedupe(results):
    keep = []
    for r in sorted(results, key=lambda r: (-r.score, r.start)):
        if not any(o.start < r.end and r.start < o.end for o in keep):
            keep.append(r)
    return sorted(keep, key=lambda r: r.start)


def _utf8_console() -> None:
    """Windows consoles default to a legacy code page; Arabic text would crash the script."""
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file")
    ap.add_argument("--outdir", help="where to write the two output files (default: next to the input)")
    ap.add_argument("--threshold", type=float, default=0.4)
    ap.add_argument("--deny", help="file with extra names or words to always mask, one per line")
    a = ap.parse_args()

    src = pathlib.Path(a.file)
    outdir = pathlib.Path(a.outdir) if a.outdir else src.parent
    outdir.mkdir(parents=True, exist_ok=True)
    con = Console()

    with con.status("Presidio is reading the Word document on this laptop (nothing is sent anywhere)…"):
        analyzer, anonymizer = build_analyzer(load_deny(a.deny)), AnonymizerEngine()
        found_doc, masked_doc = Document(src), Document(src)
        counts, items = collections.Counter(), []
        for pf, pm in zip(paragraphs(found_doc), paragraphs(masked_doc)):
            text = pf.text
            if not text.strip():
                continue
            res = dedupe([r for r in find_pii(analyzer, text, a.threshold) if r.entity_type != "DATE_TIME"])
            if not res:
                continue
            found, masked, pos = [], [], 0
            for r in res:
                if r.start > pos:
                    found.append((text[pos:r.start], None)); masked.append((text[pos:r.start], None))
                found.append((text[r.start:r.end], "found"))
                masked.append((f"<{r.entity_type}>", "label"))
                counts[r.entity_type] += 1
                items.append((text[r.start:r.end], r.entity_type, r.score))
                pos = r.end
            if pos < len(text):
                found.append((text[pos:], None)); masked.append((text[pos:], None))
            rewrite(pf, found)
            rewrite(pm, masked)

    found_path = outdir / f"{src.stem}.found.docx"
    masked_path = outdir / f"{src.stem}.masked.docx"
    found_doc.save(found_path)
    masked_doc.save(masked_path)

    t = Table(title=f"Presidio found {len(items)} items in {src.name}", title_justify="left",
              header_style="bold white on navy_blue")
    t.add_column("Found", style="bold")
    t.add_column("Type")
    t.add_column("Confidence", justify="right")
    for txt, et, sc in items:
        t.add_row(txt, et, f"{sc:.0%}")
    con.print(t)
    con.print(f"[bold red]Red highlights:[/] {found_path}")
    con.print(f"[bold dark_orange]Masked copy:[/]   {masked_path}")
    con.print("[bold]Now YOU read it:[/] anything that is not highlighted was missed.")


if __name__ == "__main__":
    _utf8_console()
    main()
