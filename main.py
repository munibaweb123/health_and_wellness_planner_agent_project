import asyncio
from agents import Runner, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from agent import health_agent
from config import config
from context import UserSessionContext
from openai.types.responses import ResponseTextDeltaEvent
from rich.console import Console
from rich.markdown import Markdown

console = Console()

async def main():
    user_context = UserSessionContext(
        name="Muniba",
        uid=1,
        goal={"target": "Lose 2kg weight"},
        diet_preferences="Keto",
        workout_plan=None,
        meal_plan=None,
        injury_notes=None,
        handoff_logs=[],
        progress_logs=[]
    )

    try:
        response = Runner.run_streamed(
            health_agent,
            "I wanna lose 2kg weight as a job worker, I prefer vegetarian diet, suggest some workout plan and meal plan",
            context=user_context,
            run_config=config
        )

        console.print("\n[bold cyan]🔹 Agent is thinking...[/bold cyan]\n")

        full_text = ""

        async for event in response.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                delta = event.data.delta.strip()
                if delta:
                    console.print(delta, end="", soft_wrap=True)
                    full_text += delta

        console.print("\n\n[bold green]✅ Final Output:[/bold green]\n")
        console.print(Markdown(full_text))

    except InputGuardrailTripwireTriggered as e:
        console.print(f"\n[bold red]❌ Input guardrail triggered:[/bold red] {e}")

    except OutputGuardrailTripwireTriggered as e:
        console.print(f"\n[bold red]❌ Output guardrail triggered:[/bold red] {e}")

if __name__ == "__main__":
    asyncio.run(main())
