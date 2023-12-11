from fastapi import FastAPI

from fraude.db import DbClient
from fraude.constants import DB_URL, DB_NAME
from fraude.models import ConversationHeaders, CreateConversation, StoredConversation


app = FastAPI()

# todo inject db_client
db_client = DbClient(DB_URL, DB_NAME)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/conversations/user/{user}")
async def get_conversations(user: str) -> ConversationHeaders:
    return db_client.get_conversation_headers(user)


@app.post("/api/conversations/user/{user}")
async def get_conversations(
    conversation: CreateConversation,
    user: str,
) -> StoredConversation:
    return db_client.add_conversation(conversation, user)


if __name__ == "__main__":
    import logging
    import uvicorn

    logging.basicConfig(level=logging.INFO)

    uvicorn.run(
        "fraude.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
