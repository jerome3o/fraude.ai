# This is a simple response to the messages so far

from typing import List

from anthropic import AI_PROMPT, HUMAN_PROMPT

from fraude.models import StoredMessage, ParticipantType, WsPartialResponseMessage
from fraude.agent.models import Action, History, PartialResponseFunction
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
    for message in message_thread:
        message_prompt = (
            AI_PROMPT if message.type == ParticipantType.AI else HUMAN_PROMPT
        )
        s += f"{message_prompt} {message.content}"

    s += f"{AI_PROMPT}"
    return s


async def run_respond_action(
    history: History,
    ai_client: AiClient,
    partial_response_function: PartialResponseFunction,
) -> str:
    prompt = build_conversation_prompt(history.message_thread)

    response = ""

    async for token in ai_client.stream_completion(prompt):
        response += token
        # TODO: don't really need to await the response here?
        await partial_response_function(WsPartialResponseMessage(content=token))

    return response


respond_action = Action(
    title="Respond",
    description="Send a response to the human",
    run=run_respond_action,
)
