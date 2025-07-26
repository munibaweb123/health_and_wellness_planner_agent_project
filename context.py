from typing import Dict, List, Optional
from pydantic import BaseModel

class MealDay(BaseModel):
    day: str
    meals: List[str]  # e.g., ["Breakfast - Avocado toast", "Lunch - Grilled chicken", "Dinner - Salad"]

class MealPlan(BaseModel):
    days: List[MealDay]  # 7-day plan, each with meals for the day

class WorkoutPlan(BaseModel):
    days: List[str]         # e.g., ["Monday: Walk", "Tuesday: Yoga", ...]
    intensity: str   
class UserSessionContext(BaseModel):
    name: str
    uid: int
    goal: Optional[dict] = None
    diet_preferences: Optional[str] = None
    workout_plan: Optional[dict] = None
    meal_plan: Optional[List[str]] = None
    injury_notes: Optional[str] = None
    handoff_logs: List[str] = []
    progress_logs: List[Dict[str, str]] = []