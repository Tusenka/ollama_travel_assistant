import json
from abc import ABC, abstractmethod
from argparse import ArgumentError
from datetime import date


class LLMClient(ABC):
    @abstractmethod
    async def extract_rag(self, history: list, system_prompt: str, lang="en") -> dict:
        raise NotImplemented()

    @abstractmethod
    async def generate_response(
        self, history: list, system_prompt: str, lang="en"
    ) -> dict:
        raise NotImplemented()

    @staticmethod
    def safe_json(text: str) -> dict:
        result = LLMClient._try_load_json(text)
        if result is not None:
            return result
        if "{" in text:
            result = LLMClient._try_load_json(
                ("{" + text.split("{", 1)[1]).rsplit("}", 1)[0] + "}"
            )
        if result is not None:
            return result
        raise ArgumentError(
            None, f"Unable to parse json {text} - check the format json"
        )

    @staticmethod
    def _try_load_json(text: str) -> dict | None:
        try:
            return json.loads(text)
        except ValueError as e:
            return None
