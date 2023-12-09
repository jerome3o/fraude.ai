from pymongo import MongoClient

from fraude.models import (
    CreateConversation,
    CreateMessage,
    StoredConversation,
    StoredMessage,
)
from fraude.helpers import generate_id


# There is only the conversations collection in the database


class DbClient:
    def __init__(
        self,
        url: str,
        db_name: str,
    ):
        self.client = MongoClient(url)
        self.db = self.client[db_name]

    def get_conversation_headers(self, user_id: str) -> list[tuple[str, str]]:
        # returns all conversation titles and ids for a given user
        return [
            (conversation["_id"], conversation["title"])
            for conversation in self.db.conversations.find({"user_id": user_id})
        ]

    def get_conversation(self, conversation_id: str) -> StoredConversation:
        # returns a conversation for a given id
        conversation = self.db.conversations.find_one({"_id": conversation_id})
        return StoredConversation(**conversation)

    def add_conversation(self, conversation: CreateConversation) -> StoredConversation:
        # creates a conversation
        return StoredConversation(
            title=conversation.title,
            user_id=conversation.user_id,
        )

    def add_message(self, message: CreateMessage) -> StoredMessage:
        # gets the conversation
        conversation = self.get_conversation(message.conversation_id)

        # creates the message
        new_message = StoredMessage(
            id=generate_id(),
            type=message.type,
            content=message.content,
            responses=[],
        )

        # find parent message
        parent_message = conversation.find_message(message.parent_message_id)
        parent_message.responses.append(new_message)

        # update conversation
        self.db.conversations.update_one(
            {"_id": conversation._id}, {"$set": conversation.model_dump()}
        )

        return new_message