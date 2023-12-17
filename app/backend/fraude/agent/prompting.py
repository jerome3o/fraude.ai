from anthropic import HUMAN_PROMPT, AI_PROMPT

from fraude.models import StoredMessage, ParticipantType
from fraude.models import Action, History

_PROMPT_TEMPLATE = f"""\
You are a helpful AI agent called Fraude, who is in dialogue with a human, as an AI agent you are \
able to perform a list of actions:

{{action_descriptions}}

To perform an action you must simply respond with the action key and that is all.

Following is the conversation so far:

===={{context}}

===={HUMAN_PROMPT} What action would you like to perform? Please choose from {{action_list}}. \
Only respond with the name of the action, Do not write anything more than that, only one of the \
action keys and nothing more. I will give you further instruction once you have decided.{AI_PROMPT}
"""


def build_thread_prompt(message_thread: list[StoredMessage]) -> str:
    s = ""
    for message in message_thread:
        message_prompt = (
            AI_PROMPT if message.type == ParticipantType.AI else HUMAN_PROMPT
        )
        s += f"{message_prompt} {message.content}"

    return s


def _build_action_list(actions: list[Action]) -> str:
    if len(actions) == 1:
        return f'"{actions[0].title}"'

    if len(actions) == 2:
        return f'"{actions[0].title}" or "{actions[1].title}"'

    return (
        ", ".join([f'"{action.title}"' for action in actions[:-1]])
        + f', or "{actions[-1].title}"'
    )


def _build_action_descriptions(actions: list[Action]) -> str:
    return "\n".join([f"{action.title}: {action.description}" for action in actions])


def build_agent_prompt(
    actions: list[Action],
    history: History,
) -> str:
    action_list = _build_action_list(actions)
    action_descriptions = _build_action_descriptions(actions)
    context = build_thread_prompt(history.message_thread)

    return _PROMPT_TEMPLATE.format(
        context=context,
        action_list=action_list,
        action_descriptions=action_descriptions,
    )
