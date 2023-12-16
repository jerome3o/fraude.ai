from __future__ import annotations

from typing import List, Optional
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
