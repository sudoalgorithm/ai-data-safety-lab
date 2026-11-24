# /// script
# requires-python = ">=3.10,<3.13"
# dependencies = [
#   "presidio-analyzer",
#   "presidio-anonymizer",
#   "en_core_web_lg @ https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.8.0/en_core_web_lg-3.8.0-py3-none-any.whl",
# ]
# ///
"""Claude Code UserPromptSubmit hook: block prompts that contain personal data.

Claude Code sends the hook a JSON object on stdin with a "prompt" field.
Exit code 2 blocks the prompt and shows stderr to the user.
Exit code 0 lets it through.

Generic names and locations are not blocked here because they produce many
false positives in normal requirements text; IDs, phones, emails, IBANs,
and cards are blocked.
"""

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from gcc_presidio import build_analyzer, find_pii  # noqa: E402

BLOCK = {
    "AE_EMIRATES_ID", "SA_NATIONAL_ID", "QA_QID", "KW_CIVIL_ID", "OM_CIVIL_ID",
    "BH_CPR", "GCC_PHONE", "PHONE_NUMBER", "EMAIL_ADDRESS", "IBAN_CODE",
    "CREDIT_CARD",
}
THRESHOLD = 0.5


def main() -> int:
    try:
        prompt = json.load(sys.stdin).get("prompt", "")
    except json.JSONDecodeError:
        return 0  # never break the session on a malformed payload

    found = [r for r in find_pii(build_analyzer(), prompt, THRESHOLD)
             if r.entity_type in BLOCK]
    if not found:
        return 0

    kinds = sorted({r.entity_type for r in found})
    print(
        "Blocked: this prompt looks like it contains personal data "
        f"({', '.join(kinds)}). Mask it first with "
        "`uv run presidio/mask.py`, or replace it with a synthetic "
        "example. See README.md.",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main())
