import logging
from abc import ABC, abstractmethod

from anthropic import AsyncAnthropic

_logger = logging.getLogger(__name__)


class AiClient(ABC):
    @abstractmethod
    async def completion(self, prompt: str) -> str:
        pass


class AnthropicClient(AiClient):
    def __init__(self, api_key: str):
        self._client = AsyncAnthropic(api_key=api_key)

    async def completion(self, prompt: str) -> str:
        _logger.info(f"Running completion:\n===== {prompt}\n======")
        resp = await self._client.completions.create(
            model="claude-2",
            max_tokens_to_sample=300,
            prompt=prompt,
        )
        return resp.completion
