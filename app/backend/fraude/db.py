import datetime

from pymongo import MongoClient
from bson.objectid import ObjectId

from fraude.models import (
    ConversationHeaders,
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

    def get_conversation_headers(self, user_id: str) -> ConversationHeaders:
        # returns all conversation titles and ids for a given user
        return [
            (str(conversation["_id"]), conversation["title"])
            for conversation in self.db.conversations.find({"user_id": user_id})
        ]

    def get_conversation(self, conversation_id: str) -> StoredConversation:
        # returns a conversation for a given id
        conversation = self.db.conversations.find_one(
            {"_id": ObjectId(conversation_id)}
        )
        return StoredConversation(**conversation)

    def add_conversation(
        self, conversation: CreateConversation, user: str
    ) -> StoredConversation:
        # creates a conversation
        time_string = datetime.datetime.now().isoformat()
        convo = StoredConversation(
            title=conversation.title,
            user_id=user,
            created_at=time_string,
            updated_at=time_string,
        )

        # adds the conversation to the database
        value = self.db.conversations.insert_one(convo.model_dump())

        convo.id = str(value.inserted_id)

        return convo

    def add_message(
        self,
        message: CreateMessage,
        convo: str,
    ) -> StoredMessage:
        # gets the conversation
        conversation = self.get_conversation(convo)

        # creates the message
        new_message = StoredMessage(
            conversation_id=convo,
            id=generate_id(),
            type=message.type,
            content=message.content,
            responses=[],
        )

        if message.parent_message_id is None:
            # add to conversation
            conversation.messages.append(new_message)
        else:
            # find parent message
            parent_message = conversation.find_message(message.parent_message_id)

            if parent_message is None:
                raise ValueError("parent message not found")

            parent_message.responses.append(new_message)

        # update conversation
        self.db.conversations.update_one(
            {"_id": ObjectId(conversation.id)},
            {"$set": conversation.model_dump()},
        )

        return new_message
