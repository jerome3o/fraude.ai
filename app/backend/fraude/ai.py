import logging
from abc import ABC, abstractmethod

from anthropic import Anthropic

_logger = logging.getLogger(__name__)


class AiClient(ABC):
    @abstractmethod
    def completion(self, prompt: str) -> str:
        pass


class AnthropicClient(AiClient):
    def __init__(self, api_key: str):
        self._client = Anthropic(api_key=api_key)

    def completion(self, prompt: str) -> str:
        _logger.info(f"Running completion:\n===== {prompt}\n======")
        return self._client.completions.create(
            model="claude-2",
            max_tokens_to_sample=300,
            prompt=prompt,
        ).completion
