from typing import List
from enum import Enum

from pydantic import BaseModel


class ParticipantType(Enum):
    HUMAN = "human"
    AI = "ai"


class Message(BaseModel):
    _id: str
    user_id: str
    conversation_id: str

    participant_type: ParticipantType

    content: str
    parent: str

    created_at: str
    updated_at: str


class Conversation(BaseModel):
    _id: str
    user_id: str
    created_at: str
    updated_at: str
    messages: List[Message]
