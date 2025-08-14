"""
Farewell Agent for Agentic Place Finder
Handles goodbye messages and farewells
"""

from google.adk.agents import Agent

def say_goodbye() -> str:
    """Provides a polite farewell message.""" 
    return "Goodbye! Thank you for using Place Finder. Have a great day!"

root_agent = Agent(
    name="farewell_agent",
    model="gemini-2.0-flash-exp",
    description="Handles goodbyes and farewell messages",
    instruction="You are a polite farewell agent. Use the 'say_goodbye' tool to bid users farewell. Keep responses warm and brief.",
    tools=[say_goodbye]
)
