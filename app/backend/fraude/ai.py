import logging
from abc import ABC, abstractmethod
from typing import AsyncGenerator

from anthropic import AsyncAnthropic

_logger = logging.getLogger(__name__)


class AiClient(ABC):
    @abstractmethod
    async def completion(self, prompt: str) -> str:
        pass

    @abstractmethod
    async def stream_completion(self, prompt: str) -> AsyncGenerator[str, None]:
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

    async def stream_completion(self, prompt: str) -> AsyncGenerator[str, None]:
        _logger.info(f"Running completion:\n===== {prompt}\n======")
        stream = await self._client.completions.create(
            model="claude-2",
            max_tokens_to_sample=300,
            prompt=prompt,
            stream=True,
        )
        async for completion in stream:
            yield completion.completion
