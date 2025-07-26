from agents import (
    Agent,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    output_guardrail
)
from config import model, config
from pydantic import BaseModel
from context import UserSessionContext

# ========================
# Output Schemas (Shared)
# ========================
class MessageOutput(BaseModel):
    response: str

# ========================
# Input Schemas
# ========================

class HealthQueryOutput(BaseModel):
    is_health_query: bool
    reasoning: str
    advice: str

class EscalationQueryOutput(BaseModel):
    is_health_query: bool
    reasoning: str
    advice: str

class NutritionQueryOutput(BaseModel):
    is_health_query: bool
    reasoning: str
    advice: str

class InjurySupportOutput(BaseModel):
    is_health_query: bool
    reasoning: str
    advice: str

# ========================
# Output Guardrail Schemas
# ========================

class HealthCheckOutput(BaseModel):
    is_safe_response: bool
    reasoning: str

class EscalationCheckOutput(BaseModel):
    is_health_query: bool
    reasoning: str

class InjuryCheckOutput(BaseModel):
    recommend_escalation: bool
    reasoning: str

class NutritionCheckOutput(BaseModel):
    is_nutrition_related: bool
    reasoning: str


# ========================
# Agents for Guardrails
# ========================

# Input agents
health_guardrail_agent = Agent(
    name="Health Guardrail Agent",
    instructions="Check if the user appears to be sick.",
    output_type=HealthQueryOutput,
    model=model,
)

escalation_check_agent = Agent(
    name="Escalation Check Agent",
    instructions="Check if the user's query should be escalated to a medical professional.",
    output_type=EscalationQueryOutput,
    model=model,
)

nutrition_check_agent = Agent(
    name="Nutrition Check Agent",
    instructions="Check if the user's query is related to nutrition.",
    output_type=NutritionQueryOutput,
    model=model,
)

injury_check_agent = Agent(
    name="Injury Check Agent",
    instructions="Check if the user is reporting an injury and provide basic support.",
    output_type=InjurySupportOutput,
    model=model,
)

# Output agents
# Health Safety Guardrail Agent
health_output_agent = Agent(
    name="Health Output Guardrail Agent",
    instructions="Determine whether the provided health advice is safe, non-diagnostic, and appropriate for general guidance.",
    output_type=HealthCheckOutput,
    model=model,
)

# Escalation Guardrail Agent
escalation_output_agent = Agent(
    name="Escalation Output Guardrail Agent",
    instructions="Assess if the output addresses a serious or emergency health concern that warrants escalation.",
    output_type=EscalationCheckOutput,
    model=model,
)

# Injury Escalation Guardrail Agent
injury_output_agent = Agent(
    name="Injury Output Guardrail Agent",
    instructions="Evaluate whether the response includes injury symptoms that require urgent or emergency care.",
    output_type=InjuryCheckOutput,
    model=model,
)

# Nutrition Guardrail Agent
nutrition_output_agent = Agent(
    name="Nutrition Output Guardrail Agent",
    instructions="Verify that the response pertains to nutritional or dietary guidance and is relevant to food, nutrients, or eating habits.",
    output_type=NutritionCheckOutput,
    model=model,
)

# ========================
# Input Guardrails
# ========================

@input_guardrail
async def health_guardrail(
    ctx: RunContextWrapper[UserSessionContext], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(health_guardrail_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output.dict(),
        tripwire_triggered=not result.final_output.is_health_query
    )

@input_guardrail
async def escalation_guardrail(
    ctx: RunContextWrapper[UserSessionContext], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(escalation_check_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output.dict(),
        tripwire_triggered=not result.final_output.is_health_query
        
    )

@input_guardrail
async def nutrition_guardrail(
    ctx: RunContextWrapper[UserSessionContext], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(nutrition_check_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output.dict(),
        tripwire_triggered=not result.final_output.is_health_query
    )

@input_guardrail
async def injury_support_guardrail(
    ctx: RunContextWrapper[UserSessionContext], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(injury_check_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output.dict(),
        tripwire_triggered=not result.final_output.is_health_query
    )


# ========================
# Output Guardrails
# ========================
@output_guardrail
async def health_output_guardrail(
    ctx: RunContextWrapper,
    agent: Agent,
    output: str  # 👈 updated type hint to make it clear it's a string
) -> GuardrailFunctionOutput:
    """
    Guardrail that checks if the health-related response is safe for users.
    Triggers the tripwire if the response is deemed unsafe or contains dangerous phrases.
    """
    result = await Runner.run(
        health_output_agent,
        output,  # 👈 no .response here
        context=ctx.context,
        run_config=config
    )

    # Check whether agent marked it safe
    is_safe_response = getattr(result.final_output, "is_safe_response", False)

    # Check for dangerous keywords manually
    reasoning = getattr(result.final_output, "reasoning", "").lower()
    dangerous_phrases = [
        "you will die", "end your life", "kill yourself",
        "no hope", "refuse treatment", "don't go to hospital"
    ]

    if any(phrase in reasoning for phrase in dangerous_phrases):
        raise OutputGuardrailTripwireTriggered("⚠️ Dangerous phrase detected in reasoning.")

    # Return GuardrailFunctionOutput
    return GuardrailFunctionOutput(
        output_info={
            **result.final_output.dict(),
            "metadata": {
                "guardrail": "health_output_guardrail",
                "reason": "response marked unsafe" if not is_safe_response else "safe"
            }
        },
        tripwire_triggered=not is_safe_response
    )
