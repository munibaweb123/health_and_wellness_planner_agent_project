from agents import Agent
from config import model
from tools.meal_planner import meal_planner
from tools.goal_analyzer import analyze_goal
from tools.schedular import schedular
from tools.workout_recommender import workout_recommender
from tools.tracker import tracker

nutrition_expert_agent = Agent(
    name="nutrition_expert_agent",
    instructions="You are a nutrition expert. Provide detailed meal plans and dietary advice based on health goals.",
    tools=[meal_planner, analyze_goal, schedular, workout_recommender, tracker],
    model=model
)