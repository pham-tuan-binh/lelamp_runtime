#!/usr/bin/env python3
"""
Simple LiveKit test script for testing Cerebras LLM with OpenAI voice services.
Run this script to test your LiveKit configuration without the full LeLamp setup.
"""

from dotenv import load_dotenv
import asyncio
import logging

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, function_tool
from livekit.plugins import openai, noise_cancellation, silero, groq

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestAgent(Agent):
    """Simple test agent for LiveKit testing"""
    
    def __init__(self):
        super().__init__(instructions="""
        You are a helpful test assistant. You can help with basic questions and tasks.
        Keep your responses concise and friendly. You're here to test the LiveKit integration
        with Cerebras LLM and OpenAI voice services.
        
        You have access to several tools that you can use to help users:
        - get_current_time: Get the current date and time
        - calculate: Perform basic math calculations
        - echo_message: Echo back a message (useful for testing)
        - get_weather_info: Get basic weather information (mock data for testing)
        """)
    
    @function_tool
    async def get_current_time(self) -> str:
        """Get the current date and time for testing purposes"""
        import datetime
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"Current time is: {current_time}"
    
    @function_tool
    async def calculate(self, expression: str) -> str:
        """Perform basic math calculations safely"""
        try:
            # Simple validation - only allow basic math operations
            allowed_chars = set('0123456789+-*/.() ')
            if not all(c in allowed_chars for c in expression):
                return "Error: Only basic math operations (+, -, *, /, parentheses) and numbers are allowed"
            
            # Use a safer evaluation method
            import ast
            result = ast.literal_eval(expression)
            return f"Result: {expression} = {result}"
        except Exception as e:
            return f"Error calculating '{expression}': {str(e)}"
    
    @function_tool
    async def echo_message(self, message: str) -> str:
        """Echo back a message - useful for testing tool calling"""
        return f"Echo: {message}"
    
    @function_tool
    async def get_weather_info(self, city: str) -> str:
        """Get basic weather information (mock data for testing)"""
        if not city:
            city = "San Francisco"
            
        # Mock weather data for testing
        mock_weather = {
            "San Francisco": "Sunny, 72°F",
            "New York": "Cloudy, 65°F", 
            "London": "Rainy, 55°F",
            "Tokyo": "Clear, 78°F",
            "Paris": "Partly cloudy, 68°F"
        }
        
        weather = mock_weather.get(city, "Unknown city")
        return f"Weather in {city}: {weather} (Note: This is mock data for testing)"

async def entrypoint(ctx: agents.JobContext):
    """Entry point for the LiveKit agent"""
    logger.info("Starting LiveKit test agent...")
    
    # Create the test agent
    agent = TestAgent()
    
    # Configure the session with Cerebras LLM and OpenAI voice services
    session = AgentSession(
        llm=groq.LLM(
            model="openai/gpt-oss-120b"
        ),
        stt = openai.STT(
            model="gpt-4o-transcribe",
        ),
        tts = openai.TTS(
            model="gpt-4o-mini-tts",
            voice="ballad",
            instructions="Speak in a friendly and conversational tone.",
        ),
        vad=silero.VAD.load(),
    )
    
    logger.info("Agent session configured with Cerebras LLM and OpenAI voice")
    
    # Start the session
    await session.start(
        room=ctx.room,
        agent=agent,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )
    
    logger.info("Session started successfully")
    
    # Generate an initial greeting
    await session.generate_reply(
        instructions="Say hello and introduce yourself as a test assistant. Keep it brief and friendly."
    )

def main():
    """Main function to run the LiveKit agent"""
    logger.info("Starting LiveKit test script...")
    
    # Run the agent with LiveKit CLI
    agents.cli.run_app(
        agents.WorkerOptions(
            entrypoint_fnc=entrypoint,
            num_idle_processes=1
        )
    )

if __name__ == "__main__":
    main()
