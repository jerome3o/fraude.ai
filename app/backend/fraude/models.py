from __future__ import annotations

from typing import List, Optional
from enum import Enum

from pydantic import BaseModel


def _find_message(messages: List[StoredMessage], message_id: str) -> StoredMessage:
    for message in messages[::-1]:
        if message.id == message_id:
            return message
        elif message.responses:
            found_message = _find_message(message.responses, message_id)
            if found_message:
                return found_message

    return None


class ParticipantType(Enum):
    HUMAN = "human"
    AI = "ai"


class Message(BaseModel):
    type: ParticipantType
    content: str


class CreateMessage(Message):
    parent_message_id: str
    conversation_id: str


class StoredMessage(Message):
    # this will be created by db client
    id: str
    responses: List[StoredMessage]


class Conversation(BaseModel):
    user_id: str
    title: str


class CreateConversation(Conversation):
    pass


class StoredConversation(Conversation):
    # database will provide this
    _id: Optional[str] = None

    created_at: str
    updated_at: str

    messages: List[StoredMessage]

    def find_message(self, message_id: str) -> Optional[StoredMessage]:
        return _find_message(self.messages, message_id)
