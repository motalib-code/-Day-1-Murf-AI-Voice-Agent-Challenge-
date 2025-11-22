import logging
import json
from typing import Annotated, List, Optional, TypedDict

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    WorkerOptions,
    cli,
    metrics,
    tokenize,
    function_tool,
    RunContext
)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")

class OrderDetails(TypedDict):
    drinkType: str
    size: str
    milk: str
    extras: List[str]
    name: str

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a friendly barista at "CodeBrew Coffee".
            Your goal is to take the user's order efficiently and kindly.
            You must fill out the following order details: drinkType, size, milk, extras (optional), and the customer's name.

            Ask clarifying questions to get the missing information.
            Start by greeting the customer and asking what they would like.

            Once you have all the necessary details (drinkType, size, milk, name), verify the order with the user.
            If they confirm, use the 'submit_order' tool to finalize the order.
            Use 'update_order' to update the order state as you get information.
            """,
        )
        self.order_state: OrderDetails = {
            "drinkType": "",
            "size": "",
            "milk": "",
            "extras": [],
            "name": ""
        }

    @function_tool
    async def update_order(
        self,
        ctx: RunContext,
        drink_type: Annotated[Optional[str], "The type of drink (e.g., Latte, Cappuccino)"] = None,
        size: Annotated[Optional[str], "The size of the drink (e.g., Small, Medium, Large)"] = None,
        milk: Annotated[Optional[str], "The type of milk (e.g., Whole, Oat, Almond)"] = None,
        extras: Annotated[Optional[List[str]], "Any extras (e.g., sugar, syrup)"] = None,
        name: Annotated[Optional[str], "The customer's name"] = None
    ):
        """
        Update the current order details. Only provide fields that need to be updated.
        """
        if drink_type:
            self.order_state["drinkType"] = drink_type
        if size:
            self.order_state["size"] = size
        if milk:
            self.order_state["milk"] = milk
        if extras is not None:
            self.order_state["extras"] = extras
        if name:
            self.order_state["name"] = name

        logger.info(f"Order updated: {self.order_state}")
        return f"Order updated. Current state: {self.order_state}"

    @function_tool
    async def submit_order(self, ctx: RunContext):
        """
        Finalize and submit the order. Call this only when all details (drinkType, size, milk, name) are confirmed.
        """
        # Check if required fields are present
        required = ["drinkType", "size", "milk", "name"]
        missing = [field for field in required if not self.order_state[field]]

        if missing:
            return f"Cannot submit order. Missing details: {', '.join(missing)}. Please ask the user for these."

        filename = "order.json"
        with open(filename, "w") as f:
            json.dump(self.order_state, f, indent=2)

        logger.info(f"Order submitted: {self.order_state}")
        return "Order submitted successfully!"


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
                text_pacing=True
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
