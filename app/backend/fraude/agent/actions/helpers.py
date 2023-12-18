from typing import Awaitable, Callable
from fraude.models import AiClient, WsPartialResponseMessage


async def stream_response_back(
    prompt: str,
    ai_client: AiClient,
    callback: Callable[[str], Awaitable[None]],
    **kwargs,
) -> str:
    response = ""

    first = True
    async for token in ai_client.stream_completion(prompt, **kwargs):
        if first:
            token = token.lstrip(" ")
            first = False

        response += token
        # TODO: don't really need to await the response here?
        await callback(WsPartialResponseMessage(content=token))

    return response
