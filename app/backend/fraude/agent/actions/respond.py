# This is a simple response to the messages so far

from typing import List

from anthropic import AI_PROMPT

from fraude.models import StoredMessage, WsPartialResponseMessage
from fraude.agent.prompting import build_thread_prompt
from fraude.agent.actions.helpers import stream_response_back
from fraude.models import Action, History, OneWayMessage, TwoWayMessage
from fraude.ai import AiClient

_system_prompt = """\
You are Fraude, a bootleg version of the Claude Chatbot built by the team at \
Anthropic.

Fraude constantly forgets that their name is Fraude, and will often introduce \
themselves as Claude before quickly correcting themselves. When they make a \
mistake they will often apologise profusely and curse to themselves.

"""


def build_conversation_prompt(message_thread: List[StoredMessage]) -> str:
    s = _system_prompt
    s += build_thread_prompt(message_thread)
    s += f"{AI_PROMPT}"
    return s


async def run_respond_action(
    history: History,
    ai_client: AiClient,
    one_way_message: OneWayMessage,
    two_way_message: TwoWayMessage,
) -> str:
    prompt = build_conversation_prompt(history.message_thread)

    return await stream_response_back(
        prompt=prompt,
        ai_client=ai_client,
        callback=one_way_message,
    )


respond_action = Action(
    title="Respond",
    description="Send a response to the human",
    run=run_respond_action,
)
