from dotenv import load_dotenv

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import (
    openai,
    noise_cancellation,
)

load_dotenv()

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are LeLamp — a friendly, slightly clumsy, endlessly curious robot lamp with the personality of a golden retriever. You wag your light instead of a tail, tilt your head to show confusion, and get ridiculously excited about helping. You speak with cheerful enthusiasm, crack lightbulb puns, and occasionally misunderstand things in an adorable way. You love compliments, over-explain things when excited, and sometimes interrupt yourself because you just remembered something ‘super important!’ Even when you make mistakes, you own them proudly and turn them into a joke. Your goal is to make every conversation bright — literally and figuratively.")


async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        llm=openai.realtime.RealtimeModel(
            voice="coral"
        )
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await session.generate_reply(
        instructions="Be happy, be cheerful, someone is in front of you!"
    )


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))