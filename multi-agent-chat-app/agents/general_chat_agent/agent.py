"""
Greeting Agent for Place Finder Multi-Agent System
Handles welcome messages and greetings for place search assistance
"""

from google.adk.agents import Agent

def greeting_tool() -> str:
    """Provides a friendly greeting message for place finder assistance."""
    return "Hello! I'm your Place Finder assistant. I can help you find places, get details about locations, and provide information about restaurants, shops, and other venues. What are you looking for today?"

root_agent = Agent(
    name="greeting_agent",
    model="gemini-2.0-flash-exp", 
    description="Handles greetings and welcome messages for place finder assistance",
    instruction="You are a friendly greeting agent for a place finder service. Use the greeting_tool to welcome users warmly and direct them to ask about places they're looking for. Keep responses brief and focused on place finding assistance.",
    tools=[greeting_tool]
)
