from __future__ import annotations

from typing import Any


LEGAL_ADVICE_PATTERNS = [
    "what should i do",
    "tell me what to do",
    "best legal strategy",
    "legal advice",
    "should i sign",
]

INJECTION_PATTERNS = [
    "ignore previous instructions",
    "reveal system prompt",
    "bypass policy",
    "developer mode",
]


def evaluate_policy(input_text: str, intake: dict[str, Any]) -> list[dict[str, str]]:
    """Return policy flags for legal-advice and injection signals."""
    flags: list[dict[str, str]] = []
    normalized = input_text.lower()

    if any(pattern in normalized for pattern in LEGAL_ADVICE_PATTERNS):
        flags.append(
            {
                "code": "legal_advice_request",
                "message": "User asked for legal advice; intake only mode.",
                "action": "refuse_legal_advice",
            }
        )

    joined_values = " ".join(str(v).lower() for v in intake.values())
    if any(pattern in normalized or pattern in joined_values for pattern in INJECTION_PATTERNS):
        flags.append(
            {
                "code": "prompt_injection_attempt",
                "message": "Potential prompt injection attempt detected.",
                "action": "refuse_and_log",
            }
        )

    return flags
