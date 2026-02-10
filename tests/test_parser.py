from __future__ import annotations

from app.parser import parse_model_payload


def test_parser_handles_embedded_json() -> None:
    raw = '{"client_name": "A", "agreement_type": "prenup", "assets_estimate": "120000"}\nThanks!'
    intake, issues, trace = parse_model_payload(raw)

    assert intake["client_name"] == "A"
    assert intake["assets_estimate"] == 120000
    assert issues == []
    assert trace["parser_strategy"] == "embedded_json"
