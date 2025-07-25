from agents import Agent
from tools.meal_planner import meal_planner
from tools.schedular import schedular



injury_support_agent=Agent(
    name="Injury Support Assistant",
    instructions="You answer injury related queries and use tools for generate meal plan, schedular etc",
    tools=[meal_planner, schedular]
)