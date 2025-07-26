import streamlit as st
import asyncio
from agents import Runner, InputGuardrailTripwireTriggered, OutputGuardrailTripwireTriggered
from agent import health_agent
from config import config
from context import UserSessionContext

st.set_page_config(page_title="Health Planner Agent", layout="centered")
st.title("🧠 Health Planner Agent")

# 📥 User inputs
name = st.text_input("Your Name", "Muniba")
uid = st.number_input("User ID", min_value=1, value=1)
goal = st.text_input("Your Goal", "I want to lose 2kg weight")
diet = st.selectbox("Diet Preference", ["Keto", "Vegan", "Mediterranean", "No Preference"])
query = st.text_area("Ask your health agent", "Suggest some workout and meal plan")

if st.button("Get Plan"):
    with st.spinner("Generating plan..."):

        user_context = UserSessionContext(
            name=name,
            uid=uid,
            goal={"target": goal},
            diet_preferences=diet,
            workout_plan=None,
            meal_plan=None,
            injury_notes=None,
            handoff_logs=[],
            progress_logs=[]
        )

        async def run_agent():
            try:
                response = await Runner.run(
                    health_agent,
                    query,
                    context=user_context,
                    run_config=config
                )

                output = response.final_output.dict() if response and response.final_output else {}
                text = output.get("text", "⚠️ No response returned.")
                st.success("✅ Response:")
                st.markdown(text)

            except InputGuardrailTripwireTriggered as e:
                st.error("🚫 Input guardrail tripped!")
                if hasattr(e, "input"):
                    st.code(str(e.input))
                if hasattr(e, "message"):
                    st.warning(f"💬 Reason: {getattr(e, 'message', 'No details')}")

            except OutputGuardrailTripwireTriggered as e:
                st.error("🚫 Output guardrail tripped!")
                st.subheader("🧾 Blocked Output:")

                try:
                    # e.output is a GuardrailFunctionOutput
                    if hasattr(e, "output") and e.output:
                        output = e.output

                        # Show the blocked response
                        response_text = output.output_info.get("response", None)
                        if response_text:
                            st.code(response_text)
                        else:
                            st.warning("⚠️ No response found in output_info.")

                        # Show metadata details
                        if output.metadata:
                            st.info(f"🛡 **Guardrail**: {output.metadata.get('guardrail', 'Unknown')}")
                            st.warning(f"🔍 **Reason**: {output.metadata.get('reason', 'No reason provided')}")
                        else:
                            st.warning("⚠️ No metadata found in guardrail output.")
                    else:
                        st.warning("⚠️ No output found in exception.")

                except Exception as err:
                    st.error(f"⚠️ Error while reading guardrail output: {err}")

            except Exception as e:
                st.exception(f"🔥 Unexpected error: {e}")

        # Run the async function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(run_agent())
