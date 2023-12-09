from fastapi import FastAPI

from fraude.db import DbClient
from fraude.constants import DB_URL, DB_NAME
from fraude.models import ConversationHeaders


app = FastAPI()

# todo inject db_client
db_client = DbClient(DB_URL, DB_NAME)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/conversations")
async def get_conversations() -> ConversationHeaders:
    user_id = "FAKE_USER"
    return db_client.get_conversation_headers(user_id)


if __name__ == "__main__":
    import logging
    import uvicorn

    logging.basicConfig(level=logging.INFO)

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
    )
