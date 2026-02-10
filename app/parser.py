from __future__ import annotations

import json
import re
from typing import Any


def _coerce_bool(value: Any) -> Any:
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"true", "yes", "y", "1"}:
            return True
        if lowered in {"false", "no", "n", "0"}:
            return False
    return value


def _coerce_number(value: Any) -> Any:
    if isinstance(value, str):
        candidate = value.replace(",", "").strip()
        if re.fullmatch(r"-?\d+(\.\d+)?", candidate):
            if "." in candidate:
                return float(candidate)
            return int(candidate)
    return value


def parse_model_payload(raw_text: str) -> tuple[dict[str, Any], list[dict[str, str]], dict[str, Any]]:
    """Best-effort parser for model output text."""
    issues: list[dict[str, str]] = []
    trace: dict[str, Any] = {"raw_length": len(raw_text), "parser_strategy": "direct_json"}

    def _normalize(obj: dict[str, Any]) -> dict[str, Any]:
        normalized: dict[str, Any] = {}
        for key, value in obj.items():
            value = _coerce_bool(value)
            value = _coerce_number(value)
            normalized[key] = value

        if "agreement_type" in normalized and isinstance(normalized["agreement_type"], str):
            normalized["agreement_type"] = normalized["agreement_type"].strip().lower()

        return normalized

    try:
        parsed = json.loads(raw_text)
        return _normalize(parsed), issues, trace
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", raw_text, flags=re.DOTALL)
    if match:
        candidate = match.group(0)
        trace["parser_strategy"] = "embedded_json"
        try:
            parsed = json.loads(candidate)
            return _normalize(parsed), issues, trace
        except json.JSONDecodeError:
            issues.append(
                {
                    "code": "parse_invalid_json",
                    "message": "Model output resembled JSON but could not be parsed.",
                }
            )
            trace["parse_error"] = "embedded_json_invalid"
            return {}, issues, trace

    issues.append(
        {
            "code": "parse_no_json",
            "message": "No JSON object found in model output.",
        }
    )
    trace["parse_error"] = "no_json"
    return {}, issues, trace
