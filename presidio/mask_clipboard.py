# /// script
# requires-python = ">=3.10,<3.13"
# dependencies = [
#   "presidio-analyzer",
#   "presidio-anonymizer",
#   "pyperclip",
#   "en_core_web_lg @ https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.8.0/en_core_web_lg-3.8.0-py3-none-any.whl",
# ]
# ///
"""Mask whatever is on the clipboard, in place. Copy -> run this -> paste into the AI tool.

Usage (Windows, macOS, Linux):
    uv run presidio/mask_clipboard.py
    uv run presidio/mask_clipboard.py --deny work/my-names.txt

Runs locally; nothing is sent anywhere. Always read what you paste.
On Linux it needs xclip or xsel (sudo apt install xclip).
"""

import argparse
import collections
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import pyperclip  # noqa: E402
from gcc_presidio import build_analyzer, find_pii, load_deny  # noqa: E402
from presidio_anonymizer import AnonymizerEngine  # noqa: E402
from presidio_anonymizer.entities import OperatorConfig  # noqa: E402


def _utf8_console() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--threshold", type=float, default=0.4)
    ap.add_argument("--deny", help="file with extra names or words to always mask, one per line")
    a = ap.parse_args()

    text = pyperclip.paste()
    if not text.strip():
        print("The clipboard is empty. Copy some text first.")
        return 1

    results = [r for r in find_pii(build_analyzer(load_deny(a.deny)), text, a.threshold) if r.entity_type != "DATE_TIME"]
    masked = AnonymizerEngine().anonymize(
        text=text, analyzer_results=results, operators={"DEFAULT": OperatorConfig("replace")}
    ).text
    pyperclip.copy(masked)

    counts = collections.Counter(r.entity_type for r in results)
    if counts:
        summary = ", ".join(f"{n} {t}" for t, n in counts.most_common())
        print(f"Masked {sum(counts.values())} items ({summary}). The clipboard now holds the masked text.")
    else:
        print("Nothing found to mask. The clipboard is unchanged.")
    print("Read it before you paste: names on their own and Arabic text are often missed.")
    return 0


if __name__ == "__main__":
    _utf8_console()
    sys.exit(main())
