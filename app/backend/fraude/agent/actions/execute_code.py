# this will be the agent that will generate python code to run in the browser
# This is a simple response to the messages so far

from anthropic import AI_PROMPT, HUMAN_PROMPT

from fraude.models import (
    WsExecuteCodeMessage,
    WsPartialResponseMessage,
    WsExecuteCodeResponse,
    Action,
    History,
    OneWayMessage,
    TwoWayMessage,
)
from fraude.agent.prompting import build_thread_prompt
from fraude.agent.actions.helpers import stream_response_back
from fraude.ai import AiClient

_code_generation_prompt = f"""\
You are Fraude, a code running AI. You help users by writing and running code that produces \
helpful outputs for them. When you respond with a python program, the program will be run and the \
outputs will be returned to you for further explanation. Files produced by the program will also \
available for further use.

Here is the conversation so far:

===={{context}}

===={HUMAN_PROMPT} Please write me a useful program in python that will provide helpful \
information in standard output or in files generated. {AI_PROMPT} ```python
"""

_result_interpretation_prompt = f"""\
You are Fraude, a code output interpretation AI. You help users by interpreting the outputs of \
code that has been run for them. You will be provided with the standard output of the program that \
was run. You can use this information to provide a summary of the results to the user.

Here is the conversation so far:

===={{context}}

====

Here is the program that was run:

```python
{{code}}
```

Here is the standard output of the program:

```
{{stdout}}
```

{HUMAN_PROMPT} Please interpret the results of the program that was run for you in a way that is \
useful and brief for the user (just answer their original question). {AI_PROMPT} \
"""

_STDOUT_MAX_SIZE = 500


def _build_generation_prompt(history: History):
    context = build_thread_prompt(history.message_thread)
    return _code_generation_prompt.format(context=context)


def _build_interpretation_prompt(
    history: History,
    code: str,
    code_output: WsExecuteCodeResponse,
):
    context = build_thread_prompt(history.message_thread)
    return _result_interpretation_prompt.format(
        context=context,
        code=code,
        stdout=code_output.stdout[-_STDOUT_MAX_SIZE:],
    )


async def run_execute_code_action(
    history: History,
    ai_client: AiClient,
    one_way_message: OneWayMessage,
    two_way_message: TwoWayMessage,
) -> str:
    # build prompt

    async def _update_user(content: str):
        await one_way_message(WsPartialResponseMessage(content=content))

    await _update_user("Generating python code ...\n\n```python\n")

    prompt = _build_generation_prompt(history)
    # ask AI for code
    response = await stream_response_back(
        prompt=prompt,
        ai_client=ai_client,
        callback=one_way_message,
        stop=["```", "``"],
    )

    await _update_user("```\n\n")

    # TODO(j.swannack): error handling
    code_text = response.split("```")[0]
    # TODO(j.swannack): AST check?

    await _update_user("Running code now ...\n\n")

    # send code to browser and await result
    raw_output = await two_way_message(
        WsExecuteCodeMessage.model_validate({"content": code_text})
    )

    # TODO(j.swannack): error handling
    output = WsExecuteCodeResponse.model_validate_json(raw_output)

    # TODO(j.swannack): check size of each part of the output

    await _update_user(f"Output: \n\n```\n{output.stdout[-_STDOUT_MAX_SIZE:]}```\n\n")

    await _update_user("Interpreting result ...\n\n")

    # build prompt
    prompt = _build_interpretation_prompt(history, code_text, output)

    # ask AI for interpretation
    return await stream_response_back(
        prompt=prompt,
        ai_client=ai_client,
        callback=one_way_message,
    )


execute_code_action = Action(
    title="Run Code",
    description=(
        "Run some python code - do this if you'll have to make a plot, "
        "process data, or do mathematics"
    ),
    run=run_execute_code_action,
)
