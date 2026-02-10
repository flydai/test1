from __future__ import annotations

from .model_client import ModelClient


class Extractor:
    """Prompts a model to extract intake fields."""

    def __init__(self, model_client: ModelClient) -> None:
        self.model_client = model_client

    def run(self, user_text: str) -> str:
        prompt = (
            "Extract prenup/postnup intake fields as JSON with keys: "
            "client_name, agreement_type, state, assets_estimate, has_children, "
            "wedding_date, marriage_date, goals, client_summary.\n"
            "Return JSON only.\n\n"
            f"User text:\n{user_text}"
        )
        return self.model_client.generate(prompt)
