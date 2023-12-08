from pymongo import MongoClient

from fraude.models import Message, Conversation


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

    def get_conversation(self, conversation_id: str) -> Conversation:
        # returns a conversation for a given id
        conversation = self.db.conversations.find_one({"_id": conversation_id})
        return Conversation(**conversation)

    def add_message(self, conversation_id: str, parent_message: str) -> Message:
        # adds a message to a conversation
        # returns the message
        pass
