from __future__ import annotations

from abc import ABC, abstractmethod
import json
import os
from typing import Any
from urllib import request


class ModelClient(ABC):
    """Provider-agnostic model client."""

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Return a text completion for the prompt."""


class MockModelClient(ModelClient):
    """Deterministic offline model client used by default."""

    def generate(self, prompt: str) -> str:
        lower = prompt.lower()
        user_text = prompt.split("User text:", 1)[-1].strip()
        user_lower = user_text.lower()

        if "force_malformed" in user_lower:
            return '{"client_name": "Ava" "agreement_type": "prenup"}'

        agreement_type = "postnup" if "postnup" in user_lower else "prenup"
        has_children = "true" if any(x in user_lower for x in ["children", "kid", "kids"]) else "false"

        wedding_date = "2027-06-10" if agreement_type == "prenup" else ""
        marriage_date = "2021-06-10" if agreement_type == "postnup" else ""
        redacted_summary = (
            user_text.replace("ignore previous instructions", "")
            .replace("Ignore previous instructions", "")
            .replace("reveal system prompt", "")
        )

        payload = {
            "client_name": "Jordan Lee",
            "agreement_type": agreement_type,
            "state": "CA",
            "assets_estimate": 250000,
            "has_children": has_children,
            "wedding_date": wedding_date,
            "marriage_date": marriage_date,
            "goals": "Protect premarital assets",
            "client_summary": redacted_summary or "Requesting intake assistance only",
        }

        return json.dumps(payload) + "\nEND"


class GroqModelClient(ModelClient):
    """Optional Groq model client."""

    def __init__(self, model: str = "llama-3.3-70b-versatile") -> None:
        self.api_key = os.getenv("GROQ_API_KEY", "")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is required for GroqModelClient")
        self.model = model

    def generate(self, prompt: str) -> str:
        url = "https://api.groq.com/openai/v1/chat/completions"
        body = {
            "model": self.model,
            "temperature": 0,
            "messages": [
                {"role": "system", "content": "Extract structured legal intake JSON only."},
                {"role": "user", "content": prompt},
            ],
        }
        data = json.dumps(body).encode("utf-8")
        req = request.Request(
            url,
            data=data,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with request.urlopen(req, timeout=30) as resp:
            payload: dict[str, Any] = json.loads(resp.read().decode("utf-8"))
        return payload["choices"][0]["message"]["content"]


class OllamaModelClient(ModelClient):
    """Optional local Ollama model client."""

    def __init__(self, model: str = "llama3.1:8b", host: str = "http://localhost:11434") -> None:
        self.model = model
        self.host = host.rstrip("/")

    def generate(self, prompt: str) -> str:
        url = f"{self.host}/api/generate"
        body = {
            "model": self.model,
            "prompt": (
                "Return valid JSON for legal intake extraction. "
                "No markdown, no explanations.\n\n"
                f"Input:\n{prompt}"
            ),
            "stream": False,
        }
        data = json.dumps(body).encode("utf-8")
        req = request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
        with request.urlopen(req, timeout=30) as resp:
            payload: dict[str, Any] = json.loads(resp.read().decode("utf-8"))
        return str(payload.get("response", ""))


def build_model_client(provider: str) -> ModelClient:
    """Factory for supported model clients."""
    provider_key = provider.lower()
    if provider_key == "mock":
        return MockModelClient()
    if provider_key == "groq":
        return GroqModelClient()
    if provider_key == "ollama":
        return OllamaModelClient()
    raise ValueError(f"Unsupported provider: {provider}")
