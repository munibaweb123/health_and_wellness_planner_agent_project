# tools/meal_planner.py
import asyncio
from agents import function_tool, RunContextWrapper
from context import UserSessionContext, MealPlan, MealDay
from typing import List

@function_tool
async def meal_planner(
    ctx: RunContextWrapper[UserSessionContext],
    goal: str,
    preferences: str = "",
    lifestyle: str = "",
) -> List[str]:
    """
    Returns a hardcoded 7-day meal plan and stores it in the context.
    """

    async def _meal_planner_inner(context: UserSessionContext) -> List[str]:
        print("🥗 [Tool Triggered] meal_planner (Hardcoded)")

        raw_days = [
            {"day": "Monday", "meals": ["Breakfast - Oatmeal with fruits", "Lunch - Grilled chicken salad", "Dinner - Lentil soup"]},
            {"day": "Tuesday", "meals": ["Breakfast - Greek yogurt with honey", "Lunch - Tuna wrap", "Dinner - Quinoa with veggies"]},
            {"day": "Wednesday", "meals": ["Breakfast - Smoothie with banana and peanut butter", "Lunch - Chickpea salad", "Dinner - Baked salmon with greens"]},
            {"day": "Thursday", "meals": ["Breakfast - Scrambled eggs and toast", "Lunch - Veggie bowl", "Dinner - Grilled tofu with rice"]},
            {"day": "Friday", "meals": ["Breakfast - Overnight oats", "Lunch - Turkey sandwich", "Dinner - Grilled shrimp and couscous"]},
            {"day": "Saturday", "meals": ["Breakfast - Fruit salad and nuts", "Lunch - Chicken quinoa bowl", "Dinner - Spaghetti with tomato sauce"]},
            {"day": "Sunday", "meals": ["Breakfast - Pancakes with berries", "Lunch - Grilled veggie sandwich", "Dinner - Stir-fried chicken and rice"]}
        ]

        structured_days = []
        readable_output = []

        for entry in raw_days:
            day = entry["day"]
            meals = entry["meals"]
            structured_days.append(MealDay(day=day, meals=meals))
            readable_output.append(f"{day}: {', '.join(meals)}")

        new_meal_plan = MealPlan(days=structured_days)
        context.meal_plan = [new_meal_plan.json()]

        return readable_output

    return await ctx.run(_meal_planner_inner)
