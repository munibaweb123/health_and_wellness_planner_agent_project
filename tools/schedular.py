from agents import function_tool
from pydantic import BaseModel
from typing import List

class ScheduleOutput(BaseModel):
    schedule: str

@function_tool
async def schedular(goal: str) -> ScheduleOutput:
    print("📌 [Tool Triggered] schedular")

    def generate_schedule_for_goal(goal: str) -> List[str]:
        goal = goal.lower()
        if "weight" in goal or "lose fat" in goal:
            return [
                "Monday: 30-min Cardio + Light Stretching",
                "Tuesday: Upper Body Strength + 15-min Walk",
                "Wednesday: Core Workout + Yoga",
                "Thursday: HIIT Training",
                "Friday: Full Body Strength",
                "Saturday: Outdoor Activity (Walk, Bike, Hike)",
                "Sunday: Rest + Meal Prep"
            ]
        elif "study" in goal:
            return [
                "Monday: 2 hours Math + 1 hour Review",
                "Tuesday: 2 hours Science + Flashcards",
                "Wednesday: 3 hours Mock Test",
                "Thursday: 1 hour Reading + 2 hours Problem Solving",
                "Friday: Revise Weak Topics",
                "Saturday: Practice Papers",
                "Sunday: Light Revision + Rest"
            ]
        elif "mindfulness" in goal or "mental" in goal:
            return [
                "Monday: 10-min Meditation + Journaling",
                "Tuesday: Nature Walk + Gratitude Practice",
                "Wednesday: Deep Breathing + Affirmations",
                "Thursday: Guided Meditation",
                "Friday: Yoga + Silence Practice",
                "Saturday: Creative Hobby Time",
                "Sunday: Digital Detox + Reflect"
            ]
        else:
            return [
                f"Monday to Sunday: Follow activities that support the goal '{goal}'",
                "Example: Break down the goal into daily tasks."
            ]

    schedule = generate_schedule_for_goal(goal)
    formatted_schedule = "\n".join(schedule)
    return ScheduleOutput(schedule=f"🗓️ Weekly Schedule for '{goal.title()}':\n\n{formatted_schedule}")
