from fastapi import FastAPI, WebSocket

from fraude.ai import AnthropicClient, AiClient
from fraude.db import DbClient
from fraude.constants import DB_URL, DB_NAME, API_KEY
from fraude.models import (
    ConversationHeaders,
    CreateConversation,
    CreateMessage,
    ParticipantType,
    RenameRequest,
    StoredConversation,
    WsMessage,
)
from fraude.models import Action, History
from fraude.agent.run import run_agent
from fraude.agent.actions import respond_action, execute_code_action


app = FastAPI()

# todo inject these
db_client = DbClient(DB_URL, DB_NAME)
ai_client: AiClient = AnthropicClient(API_KEY)
actions: list[Action] = [respond_action, execute_code_action]


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


@app.websocket("/api/conversations/id/{convo_id}/message")
async def add_message_ws(
    *,
    websocket: WebSocket,
    convo_id: str,
) -> StoredConversation:
    # TODO: reduce unnecessary db calls

    await websocket.accept()

    # get the first message, which should just be the create message request
    raw_message = await websocket.receive_text()
    message = CreateMessage.model_validate_json(raw_message)

    # TODO: DRY
    human_message = db_client.add_message(message, convo_id)
    conversation = db_client.get_conversation(convo_id)
    message_thread = conversation.get_message_thread(human_message.id)

    async def one_way_function(partial_response: WsMessage):
        await websocket.send_text(partial_response.model_dump_json())

    async def two_way_function(message: WsMessage) -> str:
        await websocket.send_text(message.model_dump_json())

        # TODO: filtering and validation on this message?
        #   this will need a lot more work if we use a persistent ws
        return await websocket.receive_text()

    # TODO(j.swannack): make actions selectable at runtime
    response = await run_agent(
        ai_client,
        actions,
        History(message_thread=message_thread),
        one_way_function,
        two_way_function,
    )

    await websocket.close()

    # TODO(j.swannack): find some way to link the response to the ai message
    _ = db_client.add_message(
        CreateMessage(
            type=ParticipantType.AI,
            content=response,
            parent_message_id=human_message.id,
        ),
        convo_id,
    )

    return db_client.get_conversation(convo_id)


@app.patch("/api/conversations/id/{convo_id}/rename")
async def rename_conversation(
    convo_id: str,
    rename: RenameRequest,
) -> StoredConversation:
    return db_client.rename_conversation(convo_id, rename.title)


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
