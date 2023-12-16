from typing import Awaitable, Callable
from pydantic import BaseModel

from fraude.models import StoredMessage, WsMessage
from fraude.ai import AiClient


PartialResponseFunction = Callable[[WsMessage], Awaitable[None]]


class History(BaseModel):
    message_thread: list[StoredMessage]


class Action(BaseModel):
    title: str
    description: str
    run: Callable[
        [
            History,
            AiClient,
            PartialResponseFunction,
        ],
        Awaitable[str],
    ]
