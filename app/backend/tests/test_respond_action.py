import logging
from fraude.ai import AnthropicClient
from fraude.agent.actions import respond_action
from fraude.models import History
from fraude.agent.run import run_agent
from fraude.constants import API_KEY
from fraude.models import StoredMessage


_logger = logging.getLogger(__name__)


async def main():
    # todo mock this
    ai_client = AnthropicClient(API_KEY)

    actions = [respond_action]
    history = History(
        message_thread=[
            StoredMessage(
                type="human",
                content="Hi there!",
                id="1",
                responses=[],
                conversation_id="1",
            )
        ]
    )

    async def one_way_function(message: str):
        _logger.info(message)

    async def two_way_function(message: str):
        _logger.info(message)
        return "no"

    await run_agent(
        ai_client=ai_client,
        actions=actions,
        history=history,
        one_way_message=one_way_function,
        two_way_message=two_way_function,
    )


if __name__ == "__main__":
    import logging
    import asyncio

    logging.basicConfig(level=logging.INFO)
    # main()
    asyncio.run(main())
