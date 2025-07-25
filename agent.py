from config import model
from agents import Agent
from health_agents import nutrition_expert_agent
from tools.meal_planner import meal_planner
from tools.goal_analyzer import analyze_goal
from tools.schedular import schedular
from tools.workout_recommender import workout_recommender
from tools.tracker import tracker
from health_agents.escalation_agent import escalation_agent # type: ignore
from guardrails import health_guardrail,health_output_guardrail, escalation_guardrail, nutrition_guardrail, injury_support_guardrail, escalation_output_guardrail, nutrition_output_guardrail, injury_support_output_guardrail

health_agent= Agent(
    name="health_agent",
    instructions="You are a health and wellness planner assistant. Provide accurate and helpful health and wellness guide and use tool for that. if need specialize agent guide handoff query to relevant agent.",
    tools=[meal_planner, analyze_goal, schedular, workout_recommender, tracker],
    handoffs=[escalation_agent,nutrition_expert_agent],  # Include the nutrition expert agent for handoff
    input_guardrails=[health_guardrail, escalation_guardrail, injury_support_guardrail, nutrition_guardrail],
    output_guardrails=[health_output_guardrail, escalation_output_guardrail, injury_support_output_guardrail, nutrition_output_guardrail],
    model=model
)



