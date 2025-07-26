# tools/analyze_goal.py
from agents import function_tool
from typing import Literal

@function_tool
async def analyze_goal(goal: str) -> str:
    """
    Analyzes the given health or fitness goal and provides insights or suggestions.
    
    Args:
        goal (str): The goal to analyze.
    
    Returns:
        str: Analysis of the goal.
    """
    print("📌 [Tool Triggered] analyze_goal")

    goal_lower = goal.lower()

    if not goal or len(goal.strip()) < 5:
        return "⚠️ Your goal is too vague. Please provide more details."

    insights = []

    # Check clarity
    if any(word in goal_lower for word in ["weight", "muscle", "fat", "lose", "gain", "build", "run", "walk"]):
        insights.append("✅ Your goal contains clear fitness or health-related terms.")
    else:
        insights.append("🧐 Your goal could be made more specific. Try including measurable terms like 'lose 5kg' or 'run 3km'.")
    
    # Check realism
    if "10kg in 1 week" in goal_lower or "5kg in 3 days" in goal_lower:
        insights.append("❌ This goal may be unsafe or unrealistic. Consider consulting a professional for sustainable planning.")
    elif "1-2kg per week" in goal_lower or "30 minutes daily" in goal_lower:
        insights.append("✅ This sounds like a realistic and healthy goal.")

    # Add suggestion
    insights.append("💡 Tip: Set SMART goals — Specific, Measurable, Achievable, Relevant, and Time-bound.")

    return "\n".join(insights)
