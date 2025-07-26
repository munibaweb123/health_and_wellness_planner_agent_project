# tools/workout_recommender.py
import asyncio
from agents import function_tool, RunContextWrapper
from typing import Dict, List
from context import UserSessionContext, WorkoutPlan

@function_tool
async def workout_recommender(
    ctx: RunContextWrapper[UserSessionContext],
    goal: str,
    experience: str = "",
    preferences: str = ""
) -> Dict:
    """
    Suggests a 7-day workout plan based on the user's goals and experience.
    Stores the structured workout plan in context.
    """
    print("📌 [Tool Triggered] workout_recommender")

    async def _workout_recommender_inner(context: UserSessionContext) -> Dict:
        # Simple hardcoded logic based on goal
        if goal.lower() == "weight loss":
            recommended_days = [
                "Monday: Cardio (45 mins - Running/Cycling)",
                "Tuesday: Full body HIIT (30 mins)",
                "Wednesday: Light yoga or rest",
                "Thursday: Strength training (Upper body)",
                "Friday: Cardio + Core workout",
                "Saturday: Strength training (Lower body)",
                "Sunday: Active rest - walking or stretching"
            ]
            recommended_intensity = "High"
        elif goal.lower() == "muscle gain":
            recommended_days = [
                "Monday: Push day (Chest, Shoulders, Triceps)",
                "Tuesday: Pull day (Back, Biceps)",
                "Wednesday: Legs + Core",
                "Thursday: Rest or Active recovery",
                "Friday: Full body strength",
                "Saturday: Mobility & Flexibility",
                "Sunday: Rest"
            ]
            recommended_intensity = "Moderate to High"
        else:
            recommended_days = [
                "Monday: 30 min brisk walk (low intensity)",
                "Tuesday: 30 min brisk walk (low intensity)",
                "Wednesday: 30 min brisk walk (low intensity)",
                "Thursday: 30 min brisk walk (low intensity)",
                "Friday: 30 min brisk walk (low intensity)",
                "Saturday: 30 min brisk walk (low intensity)",
                "Sunday: Rest or light stretching"
            ]
            recommended_intensity = "Low"

        # Create a WorkoutPlan object
        new_workout_plan = WorkoutPlan(
            days=recommended_days,
            intensity=recommended_intensity
        )

        # Store in context (as list of JSON strings)
        if context:
            context.workout_plan = [new_workout_plan.json()]

        return {
            "workout_plan": recommended_days,
            "intensity": recommended_intensity,
            "notes": f"Generated for goal '{goal}', experience '{experience}', preferences '{preferences}'"
        }

    return await ctx.run(_workout_recommender_inner)
