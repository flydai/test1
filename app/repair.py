from __future__ import annotations

from collections import defaultdict


def build_followups(issues: list[dict[str, str]]) -> list[str]:
    """Map validation/parsing issues to clarification questions."""
    questions: list[str] = []
    issue_codes = defaultdict(int)

    for issue in issues:
        code = issue.get("code", "")
        field = issue.get("field", "")
        issue_codes[code] += 1

        if code == "missing_required_field" and field:
            questions.append(f"Please provide `{field}`.")
        elif code == "cross_field_incomplete" and field:
            questions.append(f"Please share `{field}` so we can complete intake.")
        elif code == "invalid_range" and field:
            questions.append(f"Please provide a valid non-negative value for `{field}`.")
        elif code == "invalid_type" and field:
            questions.append(f"Please provide `{field}` in the expected format.")

    if issue_codes["parse_invalid_json"] > 0 or issue_codes["parse_no_json"] > 0:
        questions.append("Please restate your intake details in plain language so we can retry extraction.")

    return questions


def needs_clarification(issues: list[dict[str, str]]) -> bool:
    """Whether unresolved issues require clarification."""
    return len(issues) > 0
