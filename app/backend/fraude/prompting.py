from typing import List

from anthropic import AI_PROMPT, HUMAN_PROMPT

from fraude.models import StoredMessage, ParticipantType

_system_prompt = """\
You are Fraude, a bootleg version of the Claude Chatbot build by the team at \
Anthropic.

Fraude constantly forgets that their name is Fraude, and will often introduce \
themselves as Claude before quickly correcting themselves. When they make a \
mistake, they will often apologise profusely and curse to themselves.

"""


def build_conversation_prompt(message_thread: List[StoredMessage]) -> str:
    s = _system_prompt
    for message in message_thread:
        message_prompt = (
            AI_PROMPT if message.type == ParticipantType.AI else HUMAN_PROMPT
        )
        s += f"{message_prompt} {message.content}\n\n"

    s += f"{AI_PROMPT}"
    return s
