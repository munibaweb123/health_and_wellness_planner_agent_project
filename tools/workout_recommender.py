from agents import RunContextWrapper, function_tool

from context import UserSessionContext


@function_tool
async def workout_recommender(
    ctx: RunContextWrapper[UserSessionContext],
    goal: str,
    experience: str = "",
    preferences: str = ""
) -> str:
    async def _workout_recommender_inner(context: UserSessionContext) -> str:
        try:
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
                intensity = "High"
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
                intensity = "Moderate to High"
            else:
                recommended_days = [
                    "Monday: 30 min brisk walk",
                    "Tuesday: 30 min brisk walk",
                    "Wednesday: 30 min brisk walk",
                    "Thursday: 30 min brisk walk",
                    "Friday: 30 min brisk walk",
                    "Saturday: 30 min brisk walk",
                    "Sunday: Rest or light stretching"
                ]
                intensity = "Low"

            # Save in context
            plan = WorkoutPlan(days=recommended_days, intensity=intensity)
            context.workout_plan = [plan.json()]

            return (
                f"Workout Plan for goal: {goal}\n"
                f"Intensity: {intensity}\n\n" +
                "\n".join(recommended_days)
            )
        except Exception as e:
            print("❌ Tool internal error:", e)
            return "Error occurred while generating workout plan."

    return await ctx.run(_workout_recommender_inner)
