# /// script
# requires-python = ">=3.10,<3.13"
# dependencies = [
#   "presidio-analyzer",
#   "presidio-anonymizer",
#   "rich",
#   "en_core_web_lg @ https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.8.0/en_core_web_lg-3.8.0-py3-none-any.whl",
# ]
# ///
"""Live-demo view of Presidio: highlight what it found, list each finding, show the masked text.

Usage:
    uv run presidio/show_mask.py FILE [--out MASKED_FILE] [--threshold 0.4]

Uses the same GCC recognisers and settings as presidio/mask.py, so
what the audience sees is exactly what attendees get when they mask a file.
"""

import argparse
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from gcc_presidio import build_analyzer, find_pii, load_deny  # noqa: E402
from presidio_anonymizer import AnonymizerEngine  # noqa: E402
from presidio_anonymizer.entities import OperatorConfig  # noqa: E402
from rich.console import Console  # noqa: E402
from rich.panel import Panel  # noqa: E402
from rich.rule import Rule  # noqa: E402
from rich.table import Table  # noqa: E402
from rich.text import Text  # noqa: E402

GCC = {"AE_EMIRATES_ID", "SA_NATIONAL_ID", "QA_QID", "KW_CIVIL_ID", "OM_CIVIL_ID", "BH_CPR", "GCC_PHONE"}


def body_only(text: str) -> str:
    """Drop the file's own instructions (title and the '>' note) so the demo shows only the notes."""
    lines = text.splitlines()
    return "\n".join(l for l in lines if not l.startswith(">") and not l.startswith("# ")).strip() + "\n"


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
    ap.add_argument("--out", help="write the masked text here")
    ap.add_argument("--threshold", type=float, default=0.4)
    ap.add_argument("--deny", help="file with extra names or words to always mask, one per line")
    ap.add_argument("--full", action="store_true", help="keep the file's title and notes")
    a = ap.parse_args()

    con = Console(width=min(Console().width, 140))
    raw = pathlib.Path(a.file).read_text(encoding="utf-8")
    text = raw if a.full else body_only(raw)

    with con.status("Presidio is reading the text on this laptop (nothing is sent anywhere)…"):
        results = [r for r in find_pii(build_analyzer(load_deny(a.deny)), text, a.threshold) if r.entity_type != "DATE_TIME"]
        masked = AnonymizerEngine().anonymize(
            text=text, analyzer_results=results, operators={"DEFAULT": OperatorConfig("replace")}
        ).text

    # 1. original with findings highlighted
    hl = Text(text)
    for r in results:
        hl.stylize("bold white on red3" if r.entity_type != "URL" else "bold black on yellow", r.start, r.end)
    con.print(Rule("[bold]1  BEFORE: what Presidio found[/] (red = personal data, yellow = probably a false alarm)"))
    con.print(Panel(hl, border_style="red", padding=(0, 1)))

    # 2. findings table
    t = Table(title="2  What it found, and how sure it is", title_justify="left", header_style="bold white on navy_blue")
    t.add_column("Found", style="bold")
    t.add_column("Type")
    t.add_column("Confidence", justify="right")
    t.add_column("Recogniser")
    shown = []
    for r in sorted(results, key=lambda r: (-r.score, r.start)):
        if any(o.start <= r.start and r.end <= o.end for o in shown):
            continue  # same text already listed by a more confident recogniser
        shown.append(r)
    for r in sorted(shown, key=lambda r: r.start):
        src = "GCC (ours)" if r.entity_type in GCC else "Presidio built-in"
        t.add_row(text[r.start:r.end], r.entity_type, f"{r.score:.0%}", src)
    con.print(t)

    # 3. masked output
    mt = Text(masked)
    mt.highlight_regex(r"<[A-Z_]+>", "bold black on orange1")
    con.print(Rule("[bold]3  AFTER: the masked text[/] (this is what may go to an approved AI tool)"))
    con.print(Panel(mt, border_style="dark_orange", padding=(0, 1)))
    con.print(f"[bold]{len(shown)}[/] items masked.  [bold red]Now YOU read it:[/] what did it miss?")

    if a.out:
        out = pathlib.Path(a.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(masked, encoding="utf-8")
        con.print(f"Saved masked copy: [bold]{out}[/]")


if __name__ == "__main__":
    _utf8_console()
    main()
