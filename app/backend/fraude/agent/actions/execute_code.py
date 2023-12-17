# this will be the agent that will generate python code to run in the browser
# This is a simple response to the messages so far

from fraude.agent.models import Action, History, PartialResponseFunction
from fraude.ai import AiClient

_system_prompt = """\
prompt for executing code

"""


async def run_respond_action(
    history: History,
    ai_client: AiClient,
    partial_response_function: PartialResponseFunction,
) -> str:
    # build prompt
    # ask AI for code
    # send code to browser
    # get result
    # send output to claude for summarisation
    # send summary to browser
    return "nice"


respond_action = Action(
    title="Respond",
    description="Send a response to the human",
    run=run_respond_action,
)
