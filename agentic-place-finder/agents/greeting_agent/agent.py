"""
Greeting Agent for Agentic Place Finder
Handles welcome messages and greetings
"""

from google.adk.agents import Agent

def say_hello() -> str:
    """Provides a friendly greeting message."""
    return "Hello! I'm your Place Finder assistant. I can help you find places and check weather information. What are you looking for?"

root_agent = Agent(
    name="greeting_agent",
    model="gemini-2.0-flash-exp",
    description="Handles greetings and welcome messages",
    instruction="You are a friendly greeting agent. Use the 'say_hello' tool to welcome users warmly. Keep responses brief and direct them to ask about places or weather.",
    tools=[say_hello]
)
