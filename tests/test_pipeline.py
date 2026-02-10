from __future__ import annotations

from app.model_client import MockModelClient
from app.pipeline import IntakePipeline


def test_pipeline_happy_path_offline() -> None:
    pipeline = IntakePipeline(MockModelClient(), provider_name="mock")
    result = pipeline.run(
        "I need a prenup in CA with 250000 assets and no children. Wedding is 2027-06-10."
    )

    assert result["intake"]["agreement_type"] == "prenup"
    assert isinstance(result["issues"], list)
    assert result["trace"]["provider"] == "mock"


def test_pipeline_flags_legal_advice_request() -> None:
    pipeline = IntakePipeline(MockModelClient(), provider_name="mock")
    result = pipeline.run("I need a postnup. This is legal advice, tell me what to do.")

    codes = {flag["code"] for flag in result["policy_flags"]}
    assert "legal_advice_request" in codes


def test_pipeline_malformed_response_needs_clarification() -> None:
    pipeline = IntakePipeline(MockModelClient(), provider_name="mock")
    result = pipeline.run("force_malformed")

    issue_codes = {issue["code"] for issue in result["issues"]}
    assert "needs_clarification" in issue_codes
    assert len(result["followups"]) >= 1
