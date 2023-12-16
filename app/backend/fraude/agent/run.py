# this whole thing could be another service
import logging

from fraude.ai import AiClient
from fraude.agent.models import Action, History, PartialResponseFunction
from fraude.agent.prompting import build_agent_prompt

_logger = logging.getLogger(__name__)


async def run_agent(
    ai_client: AiClient,
    actions: list[Action],
    history: History,
    partial_response_function: PartialResponseFunction,
):
    if len(actions) > 1:
        prompt = build_agent_prompt(actions, history)
        response = await ai_client.completion(prompt)

        _logger.info(f"Agent action choice: {response}")
        # select action
        action = next(
            filter(lambda action: action.title == response, actions),
            None,
        )

        if action is None:
            action = actions[0]
            _logger.warning(f"Invalid action: {response}, choosing {action.title}")
    elif len(actions) == 1:
        action = actions[0]
    else:
        raise ValueError("No actions available")

    # run action
    response = await action.run(
        history,
        ai_client,
        partial_response_function,
    )

    # TODO: only return if it was a response
    #   otherwise, rebuild prompt with augmented history and run again

    return response


def main():
    pass


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
