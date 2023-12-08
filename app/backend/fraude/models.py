from __future__ import annotations

from typing import List
from enum import Enum

from pydantic import BaseModel


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
    id: str
    responses: List[StoredMessage]


class Conversation(BaseModel):
    user_id: str
    title: str


class CreateConversation(Conversation):
    pass


class StoredConversation(Conversation):
    _id: str

    created_at: str
    updated_at: str

    messages: List[StoredMessage]
