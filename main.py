import asyncio
from agents import Runner, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from agent import health_agent
from config import config
from context import UserSessionContext  # ✅ make sure context.py exists and has this class

async def main():
    # ✅ Dynamic context creation (based on your schema)
    user_context = UserSessionContext(
        name="Muniba",  # Replace with dynamic name if needed
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
        # ✅ Now pass the dynamic context
        response = await Runner.run(
            health_agent,
            "I wanna lose 2kg weight as a job worker, I prefer keto diet, suggest some workout plan and meal plan",
            context=user_context,
            run_config=config
        )
        print("✅ Output:\n", response.final_output)

    except InputGuardrailTripwireTriggered as e:
        print("🚫 Input guardrail tripped:\n", e)
    except OutputGuardrailTripwireTriggered as e:
        print("🚫 Output guardrail tripped:\n", e)

if __name__ == "__main__":
    asyncio.run(main())
