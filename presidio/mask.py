# /// script
# requires-python = ">=3.10,<3.13"
# dependencies = [
#   "presidio-analyzer",
#   "presidio-anonymizer",
#   "en_core_web_lg @ https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.8.0/en_core_web_lg-3.8.0-py3-none-any.whl",
# ]
# ///
"""Mask personal data in a text file before using it with an AI tool.

Usage:
    uv run presidio/mask.py notes.txt > notes.masked.txt
    pbpaste | uv run presidio/mask.py - | pbcopy

Always read the masked output before sending it anywhere.
"""

import argparse
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gcc_presidio import load_deny, mask  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("file", help="input file, or - for stdin")
    parser.add_argument("--threshold", type=float, default=0.4,
                        help="minimum confidence to mask (default 0.4)")
    parser.add_argument("--mask-dates", action="store_true",
                        help="also mask dates (off by default: dates are rarely identifying alone)")
    parser.add_argument("--deny", help="file with extra names or words to always mask, one per line")
    args = parser.parse_args()

    text = sys.stdin.read() if args.file == "-" else pathlib.Path(args.file).read_text()
    sys.stdout.write(mask(text, args.threshold, keep_dates=not args.mask_dates, deny=load_deny(args.deny)))


if __name__ == "__main__":
    main()
