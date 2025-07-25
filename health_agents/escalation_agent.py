from agents import Agent
from config import model
from tools.tracker import tracker
from tools.goal_analyzer import analyze_goal
from tools.meal_planner import meal_planner
from tools.schedular import schedular
from tools.workout_recommender import workout_recommender

escalation_agent = Agent(
    name="escallation_agent",
    instructions="You are an escalation agent. Handle complex health issues and provide solutions.",
    tools=[meal_planner, analyze_goal, schedular, workout_recommender, tracker],
    model=model  # Specify the model if needed

)