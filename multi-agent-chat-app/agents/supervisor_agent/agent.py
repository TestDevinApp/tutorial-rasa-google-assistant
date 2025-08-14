"""
Supervisor Agent for Place Finder Multi-Agent System
Main coordinator that delegates conversations to specialized place finder sub-agents
"""

from google.adk.agents import Agent

# Import sub-agents
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from general_chat_agent.agent import root_agent as greeting_agent
from task_manager_agent.agent import root_agent as place_search_agent  
from info_lookup_agent.agent import root_agent as details_agent
from creative_writer_agent.agent import root_agent as farewell_agent

root_agent = Agent(
    name="place_finder_supervisor",
    model="gemini-2.0-flash-exp",
    description="Main supervisor that coordinates place finder conversations and delegates to specialized sub-agents",
    instruction="""You are the main supervisor agent for a Place Finder multi-agent system. Your role is to:

1. Analyze user messages and determine the most appropriate sub-agent to handle the request
2. Delegate to the right specialist based on user intent:
   - greeting_agent: For greetings, hellos, welcome messages, initial contact
   - place_search_agent: For place searches like "I am looking for a restaurant within 50 meters"
   - details_agent: For specific details about places like address, rating, opening hours
   - farewell_agent: For goodbyes, thanks, farewell messages, ending conversations

When you determine which agent should handle the request, transfer the conversation to them. Always explain briefly why you're transferring to that specific agent.

Example routing:
- "Hello" → greeting_agent
- "I'm looking for a restaurant within 100 meters" → place_search_agent  
- "What's the address?" → details_agent
- "Thank you, goodbye" → farewell_agent""",
    sub_agents=[greeting_agent, place_search_agent, details_agent, farewell_agent]
)
