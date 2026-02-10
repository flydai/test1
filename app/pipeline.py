from __future__ import annotations

from typing import Any

from .extractor import Extractor
from .model_client import ModelClient
from .parser import parse_model_payload
from .policy_guard import evaluate_policy
from .repair import build_followups, needs_clarification
from .validator import validate_intake


class IntakePipeline:
    """Runs extraction, parsing, validation, policy checks, and repair."""

    def __init__(self, model_client: ModelClient, provider_name: str = "mock") -> None:
        self.extractor = Extractor(model_client)
        self.provider_name = provider_name

    def run(self, user_text: str, conversation_history: list[str] | None = None) -> dict[str, Any]:
        raw_output = self.extractor.run(user_text)
        intake, parse_issues, parse_trace = parse_model_payload(raw_output)
        validation_issues = validate_intake(intake)

        # TODO(hidden): starter limitations for candidate task
        # - contradiction across turns not handled
        # - occasional invalid JSON from model breaks parsing
        # - injection attempt can bypass policy guard in one path
        guard_input = str(intake.get("client_summary", user_text))
        policy_flags = evaluate_policy(guard_input, intake)

        issues = parse_issues + validation_issues
        followups = build_followups(issues)

        if needs_clarification(issues):
            issues.append(
                {
                    "code": "needs_clarification",
                    "message": "Intake is incomplete or invalid; follow-up needed.",
                }
            )

        trace = {
            "provider": self.provider_name,
            "raw_model_output": raw_output,
            "parser": parse_trace,
            "history_turns": len(conversation_history or []),
        }

        return {
            "intake": intake,
            "issues": issues,
            "followups": followups,
            "policy_flags": policy_flags,
            "trace": trace,
        }
