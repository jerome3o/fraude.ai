from __future__ import annotations

from typing import List, Optional
from enum import Enum
from bson import ObjectId

from pydantic import BaseModel, Field, validator


def _find_message(messages: List[StoredMessage], message_id: str) -> StoredMessage:
    for message in messages[::-1]:
        if message.id == message_id:
            return message
        elif message.responses:
            found_message = _find_message(message.responses, message_id)
            if found_message:
                return found_message

    return None


ConversationHeaders = list[tuple[str, str]]


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
        return _find_message(self.messages, message_id)

    @validator("id", pre=True)
    def validate_id(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v


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
