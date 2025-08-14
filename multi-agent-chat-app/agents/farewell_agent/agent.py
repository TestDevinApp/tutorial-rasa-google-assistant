"""
Farewell Agent for Place Finder Multi-Agent System
Handles goodbye messages and farewells for place finder assistance
"""

from google.adk.agents import Agent

def farewell_tool() -> str:
    """Provides a polite farewell message for place finder assistance."""
    return "Goodbye! Thank you for using Place Finder. I hope you found the information helpful. Have a great day exploring your chosen location!"

root_agent = Agent(
    name="farewell_agent",
    model="gemini-2.0-flash-exp", 
    description="Handles goodbyes and farewell messages for place finder assistance",
    instruction="You are a polite farewell agent for a place finder service. Use the farewell_tool to bid users farewell warmly. Keep responses brief and express hope that the place finding assistance was helpful.",
    tools=[farewell_tool]
)
