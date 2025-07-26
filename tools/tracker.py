from agents import function_tool
from datetime import datetime
import random

@function_tool
async def tracker(goal: str) -> str:
    """
    Tracks the user's progress toward a specific goal.
    
    Args:
        goal (str): The goal to track progress for.
    
    Returns:
        str: A formatted progress report based on the goal type.
    """
    print("📌 [Tool Triggered] tracker")

    goal = goal.lower()

    def generate_progress(goal: str) -> str:
        if "weight" in goal:
            lost = round(random.uniform(0.3, 2.0), 1)
            return f"📉 You have lost approximately {lost} kg this week. Keep up the healthy eating and workouts!"
        
        elif "study" in goal:
            hours = random.randint(8, 20)
            topics = random.randint(2, 5)
            return f"📚 You studied {hours} hours this week and completed {topics} topics. Stay consistent!"
        
        elif "muscle" in goal or "fitness" in goal:
            workouts = random.randint(3, 6)
            strength_gain = round(random.uniform(1, 3), 1)
            return f"💪 You completed {workouts} workouts and improved strength by ~{strength_gain}% this week."
        
        elif "mindfulness" in goal or "mental" in goal:
            sessions = random.randint(4, 7)
            mood_score = round(random.uniform(7.0, 9.5), 1)
            return f"🧘‍♀️ You completed {sessions} mindfulness sessions. Your average mood rating is {mood_score}/10."

        else:
            return f"✅ Tracking is enabled, but detailed progress isn't available for '{goal}' yet. Keep going!"

    progress_report = generate_progress(goal)
    return f"📈 **Progress Report for '{goal.title()}'** ({datetime.now().strftime('%Y-%m-%d')}):\n\n{progress_report}"
