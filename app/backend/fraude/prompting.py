from typing import List

from anthropic import AI_PROMPT, HUMAN_PROMPT

from fraude.models import StoredMessage, ParticipantType


def build_conversation_prompt(message_thread: List[StoredMessage]) -> str:
    s = ""
    for message in message_thread:
        message_prompt = (
            AI_PROMPT if message.type == ParticipantType.AI else HUMAN_PROMPT
        )
        s += f"{message_prompt} {message.content}\n"

    s += f"{AI_PROMPT} "
    return s
