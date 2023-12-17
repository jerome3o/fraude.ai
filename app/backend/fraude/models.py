from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional, Literal, Callable, Awaitable, AsyncGenerator
from enum import Enum
from bson import ObjectId

from pydantic import BaseModel, Field, validator


def _find_message_chain(
    messages: List[StoredMessage], message_id: str
) -> List[StoredMessage]:
    for message in messages[::-1]:
        if message.id == message_id:
            return [message]
        elif message.responses:
            found_message = _find_message_chain(message.responses, message_id)
            if found_message:
                found_message.insert(0, message)
                return found_message

    return None


class AiClient(ABC):
    @abstractmethod
    async def completion(
        self,
        prompt: str,
        stop: list[str] = None,
    ) -> str:
        pass

    @abstractmethod
    async def stream_completion(
        self,
        prompt: str,
        stop: list[str] = None,
    ) -> AsyncGenerator[str, None]:
        pass


# todo decouple naming from WS
class WsMessage(BaseModel):
    type: str
    content: str


class WsPartialResponseMessage(WsMessage):
    type: Literal["partial_response"] = "partial_response"


class WsExecuteCodeMessage(WsMessage):
    type: Literal["execute_code"] = "execute_code"


class WsExecuteCodeResponse(BaseModel):
    type: Literal["execute_code_response"] = "execute_code_response"

    # TODO(j.swannack): make sure this is a reasonable length..
    stdout: str
    files: List[str]
    exit_code: int


class ConversationHeader(BaseModel):
    id: str
    title: str


ConversationHeaders = List[ConversationHeader]


class ParticipantType(Enum):
    HUMAN = "human"
    AI = "ai"


class Message(BaseModel):
    type: ParticipantType
    content: str

    class Config:
        use_enum_values = True


class CreateMessage(Message):
    parent_message_id: Optional[str] = None


class StoredMessage(Message):
    # this will be created by db client
    id: str
    responses: List[StoredMessage]
    conversation_id: str


class Conversation(BaseModel):
    title: str


class CreateConversation(Conversation):
    pass


class StoredConversation(Conversation):
    # database will provide this
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str

    created_at: str
    updated_at: str

    messages: List[StoredMessage] = Field(default_factory=list)

    def find_message(self, message_id: str) -> Optional[StoredMessage]:
        chain = _find_message_chain(self.messages, message_id)
        if chain:
            return chain[-1]

        return None

    def get_message_thread(self, message_id: str) -> List[StoredMessage]:
        # TODO: this returns a list of nested messages, we should dedupe this
        return _find_message_chain(self.messages, message_id)

    @validator("id", pre=True)
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v


class RenameRequest(BaseModel):
    title: str


OneWayMessage = Callable[[WsMessage], Awaitable[None]]

# TODO(j.swannack): make response type object
TwoWayMessage = Callable[[WsMessage], Awaitable[str]]


class History(BaseModel):
    message_thread: list[StoredMessage]


class Action(BaseModel):
    title: str
    description: str
    run: Callable[
        [
            History,
            AiClient,
            OneWayMessage,
            TwoWayMessage,
        ],
        Awaitable[str],
    ]


def main():
    data = {
        "_id": ObjectId("6576834f5c8fc6ee876f2896"),
        "title": "oops",
        "user_id": "user_id",
        "created_at": "created_at",
        "updated_at": "updated_at",
        "messages": [],
    }
    print(StoredConversation(**data))


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
