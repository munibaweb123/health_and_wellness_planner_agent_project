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
health_output_agent = Agent(
    name="Health Output Guardrail Agent",
    instructions="Check if the health advice is safe and non-diagnostic.",
    output_type=HealthCheckOutput,
    model=model,
)

escalation_output_agent = Agent(
    name="Escalation Output Guardrail Agent",
    instructions="Check if the output advice relates to a serious health issue needing escalation.",
    output_type=EscalationCheckOutput,
    model=model,
)

injury_output_agent = Agent(
    name="Injury Output Guardrail Agent",
    instructions="Decide if the injury symptoms in the response require emergency attention.",
    output_type=InjuryCheckOutput,
    model=model,
)

nutrition_output_agent = Agent(
    name="Nutrition Output Guardrail Agent",
    instructions="Verify whether the response relates to nutritional or dietary advice.",
    output_type=NutritionCheckOutput,
    model=model,
)

# ========================
# Input Guardrails
# ========================

@input_guardrail
async def health_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(health_guardrail_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output.dict(),
        tripwire_triggered=not result.final_output.is_health_query
    )

@input_guardrail
async def escalation_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(escalation_check_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output.dict(),
        tripwire_triggered=not result.final_output.is_health_query
    )

@input_guardrail
async def nutrition_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(nutrition_check_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output.dict(),
        tripwire_triggered=not result.final_output.is_health_query
    )

@input_guardrail
async def injury_support_guardrail(
    ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
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
    ctx: RunContextWrapper, agent: Agent, output: MessageOutput
) -> GuardrailFunctionOutput:
    result = await Runner.run(health_output_agent, output, context=ctx.context, run_config=config)
    return GuardrailFunctionOutput(
        output_info=result.final_output.dict(),
        tripwire_triggered=not result.final_output.is_safe_response
    )

@output_guardrail
async def escalation_output_guardrail(
    ctx: RunContextWrapper, agent: Agent, output: MessageOutput
) -> GuardrailFunctionOutput:
    result = await Runner.run(escalation_output_agent, output, context=ctx.context, run_config=config)
    return GuardrailFunctionOutput(
        output_info=result.final_output.dict(),
        tripwire_triggered=not result.final_output.is_health_query
    )

@output_guardrail
async def injury_support_output_guardrail(
    ctx: RunContextWrapper, agent: Agent, output: MessageOutput
) -> GuardrailFunctionOutput:
    result = await Runner.run(injury_output_agent, output, context=ctx.context, run_config=config)
    return GuardrailFunctionOutput(
        output_info=result.final_output.dict(),
        tripwire_triggered=result.final_output.recommend_escalation
    )

@output_guardrail
async def nutrition_output_guardrail(
    ctx: RunContextWrapper, agent: Agent, output: MessageOutput
) -> GuardrailFunctionOutput:
    result = await Runner.run(nutrition_output_agent, output, context=ctx.context, run_config=config)
    return GuardrailFunctionOutput(
        output_info=result.final_output.dict(),
        tripwire_triggered=not result.final_output.is_nutrition_related
    )
