from agents import AsyncOpenAI, Agent, RunConfig, StreamCallback, ToolCallMessagesBuilder
from context import UserSessionContext
from rich.console import Console
from rich.markdown import Markdown

console = Console()


class RichStream(StreamCallback):
    def __init__(self):
        self._output = ""

    def on_text(self, text: str, final: bool = False):
        self._output += text
        if final:
            console.print(Markdown(self._output))

    def on_tool_call(self, tool_name: str, args: dict):
        console.print(f"[bold green]Tool Call → {tool_name}[/bold green] with args: {args}")

    def on_tool_response(self, tool_name: str, result):
        console.print(f"[bold cyan]Tool Response from {tool_name}[/bold cyan]: {result}")


async def stream_response(agent: Agent, input_text: str, ctx: UserSessionContext):
    """
    Runs an agent with streaming output.

    Args:
        agent (Agent): The agent to run.
        input_text (str): The user input string.
        ctx (UserSessionContext): The user's session context.

    Returns:
        None (prints to terminal using rich)
    """
    run_config = RunConfig(
        stream=RichStream(),
        tool_choice="auto",  # "auto" lets model decide if/when to call tools
        tool_call_messages_builder=ToolCallMessagesBuilder.auto(),
    )

    await agent.run(input_text, context=ctx, run_config=run_config)
