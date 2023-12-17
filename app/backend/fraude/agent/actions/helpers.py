from typing import Awaitable, Callable
from fraude.models import AiClient, WsPartialResponseMessage


async def stream_response_back(
    prompt: str,
    ai_client: AiClient,
    callback: Callable[[str], Awaitable[None]],
) -> str:
    response = ""

    async for token in ai_client.stream_completion(prompt):
        response += token
        # TODO: don't really need to await the response here?
        await callback(WsPartialResponseMessage(content=token))

    return response
