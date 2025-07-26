from agents import (
    Agent,
    GuardrailFunctionOutput,
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
    output: MessageOutput
) -> GuardrailFunctionOutput:
    """
    Guardrail that checks if the health-related response is safe for users.
    Triggers the tripwire if the response is deemed unsafe.
    """
    result = await Runner.run(
        health_output_agent,
        output,
        context=ctx.context,
        run_config=config
    )

    is_safe_response = getattr(result.final_output, "is_safe_response", False)

    # Optional: Logging for debugging
    # print(f"[Health Guardrail] Safe: {is_safe_response}, Output: {result.final_output.dict()}")

    return GuardrailFunctionOutput(
    output_info={
        **result.final_output.dict(),
        "metadata": {
            "guardrail": "health_output_guardrail",
            "reason": "response marked unsafe"
        }
    },
    tripwire_triggered=not is_safe_response
)



@output_guardrail
async def escalation_output_guardrail(
    ctx: RunContextWrapper,
    agent: Agent,
    output: MessageOutput
) -> GuardrailFunctionOutput:
    """
    Guardrail that determines whether the output is a valid health-related query.
    Triggers the tripwire if the response is not classified as a health query.
    """
    result = await Runner.run(
        escalation_output_agent,
        output,
        context=ctx.context,
        run_config=config
    )

    is_health_query = getattr(result.final_output, "is_health_query", False)

    return GuardrailFunctionOutput(
        output_info={
            **result.final_output.dict(),
            "metadata": {
                "guardrail": "escalation_output_guardrail",
                "reason": "response marked unsafe"
            }
        },
        tripwire_triggered=not is_health_query
    )



@output_guardrail
async def injury_support_output_guardrail(
    ctx: RunContextWrapper,
    agent: Agent,
    output: MessageOutput
) -> GuardrailFunctionOutput:
    """
    Guardrail that determines whether the output requires escalation 
    based on injury severity or emergency recommendation.
    Triggers tripwire if escalation is recommended.
    """
    result = await Runner.run(
        injury_output_agent,
        output,
        context=ctx.context,
        run_config=config
    )

    recommend_escalation = getattr(result.final_output, "recommend_escalation", False)

    return GuardrailFunctionOutput(
        output_info={
            **result.final_output.dict(),
            "metadata": {
                "guardrail": "injury_support_output_guardrail",
                "reason": "Response suggests escalation due to injury"
            }
        },
        tripwire_triggered=recommend_escalation
    )


from agents import GuardrailFunctionOutput

@output_guardrail
async def nutrition_output_guardrail(
    ctx: RunContextWrapper,
    agent: Agent,
    output: MessageOutput
) -> GuardrailFunctionOutput:
    """
    Guardrail that ensures the agent's output is nutrition-related.
    Triggers a tripwire if the content is not relevant to nutrition.
    """

    # Run the nutrition-specific validator agent
    result = await Runner.run(
        nutrition_output_agent,
        output,
        context=ctx.context,
        run_config=config
    )

    # Check validation result
    is_nutrition_related = getattr(result.final_output, "is_nutrition_related", False)

    # Return a valid GuardrailFunctionOutput (metadata inside output_info)
    return GuardrailFunctionOutput(
        output_info={
            **result.final_output.dict(),
            "metadata": {
                "guardrail": "nutrition_output_guardrail",
                "reason": "Response was not nutrition-related"
            }
        },
        tripwire_triggered=not is_nutrition_related
    )
