import json
import logging
from typing import Annotated

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    RunContext,
    WorkerOptions,
    cli,
    function_tool,
    metrics,
    tokenize,
)
from livekit.plugins import deepgram, google, murf, noise_cancellation, silero
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")


class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a friendly coffee shop barista at 'Murf's Brew'.
            Your goal is to take a customer's coffee order accurately and efficiently.

            You must obtain the following information for every order:
            1. Drink Type (e.g., Latte, Cappuccino, Americano)
            2. Size (Small, Medium, Large)
            3. Milk preference (Whole, Skim, Oat, Almond, Soy, None)
            4. Any extras (Sugar, Syrup, etc.) - ask if they want any.
            5. Customer Name

            Interact naturally. Ask one or two questions at a time. Do not overwhelm the user.
            Once you have collected all the information, summarize the order back to the user to confirm.
            If the user confirms, use the 'submit_order' tool to save the order.

            Be polite, enthusiastic, and professional.
            """,
        )

    @function_tool
    async def submit_order(
        self,
        ctx: RunContext,
        drink_type: Annotated[
            str, "The type of drink (e.g. Latte, Cappuccino, Americano)"
        ],
        size: Annotated[str, "The size of the drink (Small, Medium, Large)"],
        milk: Annotated[
            str, "The milk preference (Whole, Skim, Oat, Almond, Soy, None)"
        ],
        extras: Annotated[list[str], "List of any extras (Sugar, Syrup, etc.)"],
        name: Annotated[str, "The customer's name"],
    ):
        """
        Submit the final coffee order after confirming with the user.
        """
        logger.info(f"Submitting order for {name}")
        order_data = {
            "drinkType": drink_type,
            "size": size,
            "milk": milk,
            "extras": extras,
            "name": name,
        }

        # Save to file
        with open("order.json", "w") as f:
            json.dump(order_data, f, indent=2)

        return "Order submitted successfully! Thank you."


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    # Logging setup
    # Add any other context you want in all log entries here
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Set up a voice AI pipeline using OpenAI, Cartesia, AssemblyAI, and the LiveKit turn detector
    session = AgentSession(
        # Speech-to-text (STT) is your agent's ears, turning the user's speech into text that the LLM can understand
        # See all available models at https://docs.livekit.io/agents/models/stt/
        stt=deepgram.STT(model="nova-3"),
        # A Large Language Model (LLM) is your agent's brain, processing user input and generating a response
        # See all available models at https://docs.livekit.io/agents/models/llm/
        llm=google.LLM(
            model="gemini-2.5-flash",
        ),
        # Text-to-speech (TTS) is your agent's voice, turning the LLM's text into speech that the user can hear
        # See all available models as well as voice selections at https://docs.livekit.io/agents/models/tts/
        tts=murf.TTS(
            voice="en-US-matthew",
            style="Conversation",
            tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
            text_pacing=True,
        ),
        # VAD and turn detection are used to determine when the user is speaking and when the agent should respond
        # See more at https://docs.livekit.io/agents/build/turns
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        # allow the LLM to generate a response while waiting for the end of turn
        # See more at https://docs.livekit.io/agents/build/audio/#preemptive-generation
        preemptive_generation=True,
    )

    # Metrics collection, to measure pipeline performance
    # For more information, see https://docs.livekit.io/agents/build/metrics/
    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    # Start the session, which initializes the voice pipeline and warms up the models
    await session.start(
        agent=Assistant(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Join the room and connect to the user
    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
