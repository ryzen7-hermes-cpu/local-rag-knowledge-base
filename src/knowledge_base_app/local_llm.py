from __future__ import annotations

import requests
from typing import Any


class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "mistral"):
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(self, prompt: str, **kwargs: Any) -> str:
        payload = {"model": self.model, "prompt": prompt, "stream": False, **kwargs}
        response = requests.post(f"{self.base_url}/api/generate", json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get("response", "")

    def chat(self, messages: list[dict], **kwargs: Any) -> str:
        payload = {"model": self.model, "messages": messages, "stream": False, **kwargs}
        response = requests.post(f"{self.base_url}/api/chat", json=payload, timeout=120)
        response.raise_for_status()
        data = response.json()
        return data.get("message", {}).get("content", "")
