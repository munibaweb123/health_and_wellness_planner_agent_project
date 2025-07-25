import asyncio
from agents import Runner, InputGuardrailTripwireTriggered,OutputGuardrailTripwireTriggered
from agent import health_agent
from config import config


async def main():
    try:
        response = await Runner.run(health_agent, "I wanna loose 2kg in this week give some workout plan and meal plan, I prefer keto diet", run_config=config)
        print(response.final_output)
    except InputGuardrailTripwireTriggered as e:
        print("Input guardrail tripped: ",e)
    except OutputGuardrailTripwireTriggered as e:
        print("Output guardrail tripped: ",e)

if __name__ == "__main__":
    asyncio.run(main())