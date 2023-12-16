# TODO(j.swannack): rename this module to llm.py

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
        # The way I'm prompting is kinda bad:
        # Linter prevents trailing space on ai prompt
        # When I force it in claude gets worried and refuses to answer?
        # Solution for now is to let the AI generate it then trim it off.
        return resp.completion.lstrip(" ")

    async def stream_completion(self, prompt: str) -> AsyncGenerator[str, None]:
        _logger.info(f"Running completion:\n===== {prompt}\n======")
        stream = await self._client.completions.create(
            model="claude-2",
            max_tokens_to_sample=300,
            prompt=prompt,
            stream=True,
        )
        first = True
        async for completion in stream:
            token = completion.completion

            # See above comment
            if first:
                first = False
                token = token.lstrip(" ")

            yield completion.completion
