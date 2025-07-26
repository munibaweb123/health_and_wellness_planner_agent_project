from config import model
from agents import Agent
from health_agents.nutrition_expert_agent import nutrition_expert_agent
from tools.meal_planner import meal_planner
from tools.goal_analyzer import analyze_goal
from tools.schedular import schedular
from tools.workout_recommender import workout_recommender
from tools.tracker import tracker
from health_agents.escalation_agent import escalation_agent 
from health_agents.injury_support_agent import injury_support_agent
from guardrails import health_guardrail,health_output_guardrail, escalation_guardrail, nutrition_guardrail, injury_support_guardrail

health_agent= Agent(
    name="health_agent",
    instructions="You are a health and wellness planner assistant, and you are like superviser. use tool to Provide accurate and helpful health and wellness guide . if need specialize agent guide handoff query to relevant agent.",
    tools=[ analyze_goal,meal_planner,workout_recommender, schedular,tracker],
    handoffs=[escalation_agent,nutrition_expert_agent,injury_support_agent],  # Include the nutrition expert agent for handoff
    input_guardrails=[health_guardrail, escalation_guardrail, injury_support_guardrail, nutrition_guardrail],
    output_guardrails=[health_output_guardrail],
    model=model
)



