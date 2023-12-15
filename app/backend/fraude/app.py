from fastapi import FastAPI

from fraude.ai import AnthropicClient, AiClient
from fraude.db import DbClient
from fraude.constants import DB_URL, DB_NAME, API_KEY
from fraude.models import (
    ConversationHeaders,
    CreateConversation,
    CreateMessage,
    ParticipantType,
    StoredConversation,
    StoredMessage,
)
from fraude.prompting import build_conversation_prompt


app = FastAPI()

# todo inject these
db_client = DbClient(DB_URL, DB_NAME)
ai_client: AiClient = AnthropicClient(API_KEY)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/conversations/user/{user}")
async def get_conversations(user: str) -> ConversationHeaders:
    return db_client.get_conversation_headers(user)


@app.post("/api/conversations/user/{user}")
async def add_conversation(
    conversation: CreateConversation,
    user: str,
) -> StoredConversation:
    return db_client.add_conversation(conversation, user)


@app.get("/api/conversations/id/{convo_id}")
async def get_conversation(
    convo_id: str,
) -> StoredConversation:
    return db_client.get_conversation(convo_id)


@app.post("/api/conversations/id/{convo_id}/message")
async def add_message(
    convo_id: str,
    message: CreateMessage,
) -> list[StoredMessage]:
    # TODO: reduce unnecessary db calls

    human_message = db_client.add_message(message, convo_id)
    conversation = db_client.get_conversation(convo_id)
    message_thread = conversation.get_message_thread(human_message.id)
    prompt = build_conversation_prompt(message_thread)
    response = ai_client.completion(prompt)

    ai_message = db_client.add_message(
        CreateMessage(
            type=ParticipantType.AI,
            content=response,
            parent_message_id=human_message.id,
        ),
        convo_id,
    )

    return db_client.get_conversation(convo_id).get_message_thread(ai_message.id)


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
