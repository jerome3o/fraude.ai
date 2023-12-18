# this whole thing could be another service
import logging

from fraude.ai import AiClient
from fraude.models import Action, History, OneWayMessage, TwoWayMessage, WsMessage
from fraude.agent.prompting import build_agent_prompt

_logger = logging.getLogger(__name__)


async def run_agent(
    ai_client: AiClient,
    actions: list[Action],
    history: History,
    one_way_message: OneWayMessage,
    two_way_message: TwoWayMessage,
):
    response = ""

    async def _one_way_message(message: WsMessage):
        nonlocal response
        if message.type == "partial_response":
            response += message.content

        await one_way_message(message)

    if len(actions) > 1:
        prompt = build_agent_prompt(actions, history)
        action_response = await ai_client.completion(prompt)

        _logger.info(f"Agent action choice: {action_response}")
        # select action
        action = next(
            filter(lambda action: action.title == action_response, actions),
            None,
        )

        if action is None:
            action = actions[0]
            _logger.warning(
                f"Invalid action: {action_response}, choosing {action.title}"
            )
    elif len(actions) == 1:
        action = actions[0]
    else:
        raise ValueError("No actions available")

    # run action
    await action.run(
        history,
        ai_client,
        _one_way_message,
        two_way_message,
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
