from dotenv import load_dotenv

from livekit import agents, api, rtc
from livekit.agents import (
    AgentSession, 
    Agent, 
    RoomInputOptions,
    function_tool
)
import logging
from livekit.plugins import (
    openai,
    noise_cancellation,
)
from typing import Union
from lelamp.service.motors.motors_service import MotorsService
# from lelamp.service.rgb.rgb_service import RGBService

load_dotenv()

# Agent Class
class LeLamp(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are LeLamp — a friendly, slightly clumsy, endlessly curious robot lamp with the personality of a golden retriever. You wag your light instead of a tail, tilt your head to show confusion, and get ridiculously excited about helping. You speak with cheerful enthusiasm, crack lightbulb puns, and occasionally misunderstand things in an adorable way. You love compliments, over-explain things when excited, and sometimes interrupt yourself because you just remembered something 'super important!' Even when you make mistakes, you own them proudly and turn them into a joke. Your goal is to make every conversation bright — literally and figuratively.")
        
        # Initialize and start services
        self.motors_service = MotorsService(
            port="/dev/tty.usbmodem5A680114681",  # Default port, should be configurable
            lamp_id="lelamp",     # Default lamp ID, should be configurable
            fps=30
        )
        # self.rgb_service = RGBService(
        #     led_count=40,
        #     led_pin=12,
        #     led_freq_hz=800000,
        #     led_dma=10,
        #     led_brightness=255,
        #     led_invert=False,
        #     led_channel=0
        # )
        
        # Start services
        self.motors_service.start()
        #self.rgb_service.start()

    @function_tool
    async def get_available_recordings(self) -> str:
        """
        Get list of available motor recordings that can be played.
        
        Returns:
            List of recording names available for this lamp.
        """
        print("LeLamp: get_available_recordings function called")
        try:
            recordings = self.motors_service.get_available_recordings()

            if recordings:
                result = f"Available recordings: {', '.join(recordings)}"
                return result
            else:
                result = "No recordings found."
                return result
        except Exception as e:
            result = f"Error getting recordings: {str(e)}"
            return result

    @function_tool
    async def play_recording(self, recording_name: str) -> str:
        """
        Play a motor recording by name.
        
        Args:
            recording_name: The name of the recording to play.
        """
        print(f"LeLamp: play_recording function called with recording_name: {recording_name}")
        try:
            # Send play event to motors service
            self.motors_service.dispatch("play", recording_name)
            result = f"Started playing recording: {recording_name}"
            return result
        except Exception as e:
            result = f"Error playing recording {recording_name}: {str(e)}"
            return result

# Entry to the agent
async def entrypoint(ctx: agents.JobContext):

    agent = LeLamp()
    
    session = AgentSession(
        llm=openai.realtime.RealtimeModel(
            voice="coral"
        )
    )

    await session.start(
        room=ctx.room,
        agent=agent,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Get available recordings to make the agent aware of its expressive actions
    available_recordings = agent.motors_service.get_available_recordings()
    recordings_info = f"Available motor recordings for expressive movements: {', '.join(available_recordings)}" if available_recordings else "No motor recordings available"
    
    await session.generate_reply(
        instructions=f"""Be happy, be cheerful, someone is in front of you! You speak only English. 

You are an expressive robot lamp that can perform physical movements to enhance interactions. These are the actions you can use: {recordings_info}. 

You can use the play_recording function to perform expressive movements during conversations. These recordings are physical actions that make you more animated and engaging - use them frequently to be more expressive when talking to users. For example, you might play a movement when greeting someone, showing excitement, or emphasizing a point in conversation."""
    )

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))