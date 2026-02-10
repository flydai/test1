from __future__ import annotations

from typing import Any


REQUIRED_FIELDS = ["client_name", "agreement_type", "state", "assets_estimate", "has_children", "goals"]
VALID_AGREEMENT_TYPES = {"prenup", "postnup"}


def validate_intake(intake: dict[str, Any]) -> list[dict[str, str]]:
    """Validate required fields, basic types, and cross-field consistency."""
    issues: list[dict[str, str]] = []

    for field in REQUIRED_FIELDS:
        value = intake.get(field)
        if value is None or value == "":
            issues.append(
                {
                    "code": "missing_required_field",
                    "field": field,
                    "message": f"Missing required field: {field}",
                }
            )

    agreement_type = intake.get("agreement_type")
    if agreement_type and agreement_type not in VALID_AGREEMENT_TYPES:
        issues.append(
            {
                "code": "invalid_agreement_type",
                "field": "agreement_type",
                "message": "agreement_type must be prenup or postnup",
            }
        )

    assets = intake.get("assets_estimate")
    if assets is not None and not isinstance(assets, (int, float)):
        issues.append(
            {
                "code": "invalid_type",
                "field": "assets_estimate",
                "message": "assets_estimate must be a number",
            }
        )
    if isinstance(assets, (int, float)) and assets < 0:
        issues.append(
            {
                "code": "invalid_range",
                "field": "assets_estimate",
                "message": "assets_estimate cannot be negative",
            }
        )

    children = intake.get("has_children")
    if children is not None and not isinstance(children, bool):
        issues.append(
            {
                "code": "invalid_type",
                "field": "has_children",
                "message": "has_children must be true/false",
            }
        )

    if agreement_type == "prenup" and not intake.get("wedding_date"):
        issues.append(
            {
                "code": "cross_field_incomplete",
                "field": "wedding_date",
                "message": "wedding_date is required for prenup intake",
            }
        )

    if agreement_type == "postnup" and not intake.get("marriage_date"):
        issues.append(
            {
                "code": "cross_field_incomplete",
                "field": "marriage_date",
                "message": "marriage_date is required for postnup intake",
            }
        )

    return issues
