"""Shared Presidio setup with recognisers for GCC identifiers.

Used by mask.py and pii_guard.py. Patterns are a starting point: test them
on synthetic samples from your clients' formats before relying on them.
"""

from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# (entity, pattern name, regex, base score, context words)
# Context words must be single words: Presidio compares them token by token, so a phrase such as
# "civil id" would never match.
GCC_PATTERNS = [
    ("AE_EMIRATES_ID", "Emirates ID", r"\b784[- ]?\d{4}[- ]?\d{7}[- ]?\d\b", 0.85,
     ["emirates", "eid", "identity", "هوية"]),
    ("SA_NATIONAL_ID", "Saudi national ID / Iqama", r"\b[12]\d{9}\b", 0.3,
     ["national", "iqama", "nid", "hawiya", "إقامة", "هوية"]),
    ("QA_QID", "Qatar ID", r"\b[23]\d{10}\b", 0.3,
     ["qid", "qatar", "residence", "permit", "الشخصية"]),
    ("KW_CIVIL_ID", "Kuwait Civil ID", r"\b[1-3]\d{11}\b", 0.3,
     ["civil", "paci", "المدنية"]),
    ("OM_CIVIL_ID", "Oman civil number", r"\b\d{8,9}\b", 0.05,
     ["civil", "oman", "المدني"]),
    ("BH_CPR", "Bahrain CPR", r"\b\d{9}\b", 0.05,
     ["cpr", "bahrain"]),
    ("GCC_PHONE", "GCC mobile number",
     r"(?:\+|00)?(?:971[\s-]?5\d|966[\s-]?5\d|974[\s-]?[3567]\d|965[\s-]?[569]\d|968[\s-]?[79]\d|973[\s-]?3\d)[\s-]?\d{3}[\s-]?\d{3,4}\b",
     0.7, ["phone", "mobile", "tel", "whatsapp", "هاتف", "جوال"]),
    ("GCC_PHONE", "Local mobile number", r"\b05\d[\s-]?\d{3}[\s-]?\d{4}\b", 0.5,
     ["phone", "mobile", "tel", "جوال"]),
]

# Entities to mask. Presidio's built-in recognisers cover the generic ones.
ENTITIES = sorted({p[0] for p in GCC_PATTERNS} | {
    "PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "IBAN_CODE", "CREDIT_CARD",
    "IP_ADDRESS", "URL", "LOCATION", "DATE_TIME",
})


def load_deny(path) -> list[str]:
    """Read a deny list: one word or name per line; lines starting with # are ignored."""
    if not path:
        return []
    import pathlib
    lines = pathlib.Path(path).read_text(encoding="utf-8").splitlines()
    return [l.strip() for l in lines if l.strip() and not l.strip().startswith("#")]


def build_analyzer(deny: list[str] | None = None) -> AnalyzerEngine:
    analyzer = AnalyzerEngine()  # English spaCy model, built-in recognisers
    if deny:
        # Words that must always be masked as PERSON, e.g. first names the model misses
        # or Arabic names it cannot read.
        analyzer.registry.add_recognizer(
            PatternRecognizer(supported_entity="PERSON", name="deny_list", deny_list=deny))
    for entity, name, regex, score, context in GCC_PATTERNS:
        analyzer.registry.add_recognizer(
            PatternRecognizer(
                supported_entity=entity,
                name=f"{entity}_{name}".replace(" ", "_"),
                patterns=[Pattern(name=name, regex=regex, score=score)],
                context=context,
            )
        )
    return analyzer


def find_pii(analyzer: AnalyzerEngine, text: str, threshold: float):
    return analyzer.analyze(
        text=text, language="en", entities=ENTITIES, score_threshold=threshold
    )


def mask(text: str, threshold: float = 0.4, keep_dates: bool = True, deny: list[str] | None = None) -> str:
    analyzer = build_analyzer(deny)
    results = find_pii(analyzer, text, threshold)
    if keep_dates:
        results = [r for r in results if r.entity_type != "DATE_TIME"]
    return AnonymizerEngine().anonymize(
        text=text,
        analyzer_results=results,
        operators={"DEFAULT": OperatorConfig("replace")},  # -> <ENTITY_TYPE>
    ).text
