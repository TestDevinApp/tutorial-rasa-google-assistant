"""
Agentic Place Finder - ADK Implementation
Replicates the Rasa chatbot functionality using Google ADK and Gemini-2.5-Flash
"""

import os
import asyncio
from typing import Dict, Any, Optional
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import warnings
import logging

warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.ERROR)

MODEL_GEMINI_2_0_FLASH = "gemini-2.0-flash-exp"

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"

def get_weather_with_location(city: str, radius: str = "100") -> dict:
    """
    Retrieves weather information for a specified city within a given radius.
    
    Args:
        city (str): The name of the city (e.g., "New York", "London", "Tokyo")
        radius (str): Search radius in meters (default: "100")
    
    Returns:
        dict: Weather information with status, report, rating, address, and opening_hours
    """
    print(f"--- Tool: get_weather_with_location called for city: {city}, radius: {radius}m ---")
    
    city_normalized = city.lower().replace(" ", "")
    
    mock_places_db = {
        "newyork": {
            "status": "success",
            "report": f"The weather in New York is sunny with a temperature of 25°C. Found within {radius}m radius.",
            "rating": "4.5",
            "address": "Manhattan, New York, NY",
            "opening_hours": "Always accessible"
        },
        "london": {
            "status": "success", 
            "report": f"It's cloudy in London with a temperature of 15°C. Found within {radius}m radius.",
            "rating": "4.2",
            "address": "Central London, UK",
            "opening_hours": "Always accessible"
        },
        "tokyo": {
            "status": "success",
            "report": f"Tokyo is experiencing light rain and a temperature of 18°C. Found within {radius}m radius.",
            "rating": "4.7",
            "address": "Shibuya, Tokyo, Japan", 
            "opening_hours": "Always accessible"
        },
        "restaurant": {
            "status": "success",
            "report": f"Found a highly-rated restaurant within {radius}m radius. Weather is pleasant for dining.",
            "rating": "4.3",
            "address": "Downtown area",
            "opening_hours": "11:00 AM - 10:00 PM"
        }
    }
    
    if city_normalized in mock_places_db:
        return mock_places_db[city_normalized]
    elif city_normalized in ["restaurant", "cafe", "shop", "mall", "museum", "bank"]:
        result = mock_places_db["restaurant"].copy()
        result["report"] = f"Found a {city} within {radius}m radius. Current weather conditions are favorable."
        return result
    else:
        return {
            "status": "error",
            "error_message": f"Sorry, I don't have information for '{city}' within {radius}m radius.",
            "rating": None,
            "address": None,
            "opening_hours": None
        }

def say_hello() -> str:
    """Provides a friendly greeting message."""
    return "Hello! I'm your Place Finder assistant. I can help you find places and check weather information. What are you looking for?"

def say_goodbye() -> str:
    """Provides a polite farewell message.""" 
    return "Goodbye! Thank you for using Place Finder. Have a great day!"

def get_place_details(detail_type: str, context: str = "") -> str:
    """
    Provides specific details about a place based on the type requested.
    
    Args:
        detail_type (str): Type of detail requested ("address", "rating", "opening_hours")
        context (str): Context about the place from previous conversation
        
    Returns:
        str: The requested detail information
    """
    print(f"--- Tool: get_place_details called for {detail_type} ---")
    
    if detail_type == "address":
        return "The address is 123 Main Street, Downtown. It's about a 5-minute walk from here."
    elif detail_type == "rating":
        return "This place has a rating of 4.5 out of 5 stars based on customer reviews."
    elif detail_type == "opening_hours":
        return "The place is currently open. Opening hours are 9:00 AM to 9:00 PM, Monday through Sunday."
    else:
        return f"I can provide information about {detail_type}, but I need more context about which place you're asking about."

class AgenticPlaceFinder:
    """Main class for the Agentic Place Finder application"""
    
    def __init__(self):
        self.session_service = None
        self.runners = {}
        self.agents = {}
        self.app_name = "agentic_place_finder"
        self.user_id = "user_1"
        self.session_id = "session_001"
        
    async def initialize(self):
        """Initialize the agent system"""
        self.session_service = InMemorySessionService()
        
        self.session = await self.session_service.create_session(
            app_name=self.app_name,
            user_id=self.user_id,
            session_id=self.session_id
        )
        
        await self._create_agents()
        
        print(f"✅ Agentic Place Finder initialized successfully!")
        
    async def _create_agents(self):
        """Create all the specialized agents"""
        
        self.agents['greeting'] = Agent(
            name="greeting_agent",
            model=MODEL_GEMINI_2_0_FLASH,
            description="Handles greetings and welcome messages",
            instruction="You are a friendly greeting agent. Use the 'say_hello' tool to welcome users warmly. Keep responses brief and direct them to ask about places or weather.",
            tools=[say_hello]
        )
        
        self.agents['farewell'] = Agent(
            name="farewell_agent",
            model=MODEL_GEMINI_2_0_FLASH,
            description="Handles goodbyes and farewell messages",
            instruction="You are a polite farewell agent. Use the 'say_goodbye' tool to bid users farewell. Keep responses warm and brief.",
            tools=[say_goodbye]
        )
        
        self.agents['details'] = Agent(
            name="place_details_agent", 
            model=MODEL_GEMINI_2_0_FLASH,
            description="Provides specific details about places like address, rating, and opening hours",
            instruction="You provide specific details about places. Use 'get_place_details' tool when users ask for address, rating, or opening hours. Extract the detail type from the user's question.",
            tools=[get_place_details]
        )
        
        self.agents['main'] = Agent(
            name="place_search_agent",
            model=MODEL_GEMINI_2_0_FLASH,
            description="Main agent that handles place searches and weather queries, delegates to specialized agents",
            instruction="""You are the main Place Finder agent. Your responsibilities:

1. For place searches: Use 'get_weather_with_location' tool with the place type as 'city' and extract radius from user input (default 100m if not specified)
2. For greetings: Delegate to 'greeting_agent'  
3. For goodbyes: Delegate to 'farewell_agent'
4. For specific details (address, rating, hours): Delegate to 'place_details_agent'

When users ask "I am looking for a [PLACE] within [NUMBER] meters", extract:
- PLACE as the city parameter
- NUMBER as the radius parameter

Present search results clearly, mentioning the place found, weather conditions, and ask if they need more details.""",
            tools=[get_weather_with_location],
            sub_agents=[
                self.agents['greeting'],
                self.agents['farewell'], 
                self.agents['details']
            ]
        )
        
        for agent_name, agent in self.agents.items():
            self.runners[agent_name] = Runner(
                agent=agent,
                app_name=self.app_name,
                session_service=self.session_service
            )
            
        print(f"✅ Created {len(self.agents)} agents with runners")
        
    async def chat(self, message: str) -> str:
        """Process a chat message and return response"""
        print(f"\n>>> User: {message}")
        
        if not os.environ.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_KEY") == "test_key_for_mock_data":
            return self._get_mock_response(message)
        
        runner = self.runners['main']
        content = types.Content(role='user', parts=[types.Part(text=message)])
        
        final_response = "I'm sorry, I couldn't process your request."
        
        try:
            async for event in runner.run_async(
                user_id=self.user_id,
                session_id=self.session_id, 
                new_message=content
            ):
                if event.is_final_response():
                    if event.content and event.content.parts:
                        final_response = event.content.parts[0].text
                    elif event.actions and event.actions.escalate:
                        final_response = f"Error: {event.error_message or 'Unknown error occurred'}"
                    break
                    
        except Exception as e:
            error_str = str(e)
            if "API key not valid" in error_str or "INVALID_ARGUMENT" in error_str:
                return self._get_mock_response(message)
            final_response = f"Error processing request: {error_str}"
            
        print(f"<<< Assistant: {final_response}")
        return final_response
    
    def _get_mock_response(self, message: str) -> str:
        """Generate mock responses based on message content"""
        message_lower = message.lower()
        print(f"DEBUG: Processing message: '{message}' -> '{message_lower}'")
        
        if 'looking for' in message_lower or 'need a' in message_lower or 'find a' in message_lower:
            print("DEBUG: Detected place search")
            place_type = "restaurant"
            radius = "50"
            
            if 'restaurant' in message_lower:
                place_type = "restaurant"
            elif 'bank' in message_lower:
                place_type = "bank"
            elif 'cafe' in message_lower:
                place_type = "cafe"
            elif 'shop' in message_lower:
                place_type = "shop"
            elif 'museum' in message_lower:
                place_type = "museum"
                
            import re
            radius_match = re.search(r'(\d+)\s*meters?', message_lower)
            if radius_match:
                radius = radius_match.group(1)
            
            mock_result = get_weather_with_location(place_type, radius)
            if mock_result['status'] == 'success':
                return f"Great! I found a {place_type} within {radius} meters. {mock_result['report']} Would you like to know more details like the address, rating, or opening hours?"
            else:
                return mock_result.get('error_message', f"Sorry, I couldn't find a {place_type} within {radius} meters.")
        
        elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'greet']):
            print("DEBUG: Detected greeting")
            return "Hello! I'm your Place Finder assistant. I can help you find places and check weather information. What are you looking for?"
        
        elif any(word in message_lower for word in ['goodbye', 'bye', 'farewell', 'see you']):
            print("DEBUG: Detected goodbye")
            return "Goodbye! Thank you for using Place Finder. Have a great day!"
        
        if 'address' in message_lower:
            return get_place_details('address')
        elif 'rating' in message_lower:
            return get_place_details('rating')
        elif 'open' in message_lower or 'hours' in message_lower:
            return get_place_details('opening_hours')
        
        if 'weather' in message_lower:
            city = "London"  # Default
            if 'london' in message_lower:
                city = "London"
            elif 'new york' in message_lower:
                city = "New York"
            elif 'tokyo' in message_lower:
                city = "Tokyo"
            
            mock_result = get_weather_with_location(city)
            return mock_result['report']
        
        return "I can help you find places and check weather information. Try asking me to find a restaurant, bank, or other place within a certain radius, or ask about weather in a city!"

async def main():
    """Main function to test the agentic place finder"""
    
    if not os.environ.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_KEY") == "YOUR_GOOGLE_API_KEY":
        print("⚠️  Please set your GOOGLE_API_KEY environment variable")
        print("   Get your key from: https://aistudio.google.com/app/apikey")
        return
        
    place_finder = AgenticPlaceFinder()
    await place_finder.initialize()
    
    test_messages = [
        "Hello",
        "I am looking for a restaurant within 50 meters",
        "What's the address?", 
        "What's the rating?",
        "Is it open now?",
        "How about the weather in London?",
        "I need a bank within 200 meters",
        "Goodbye"
    ]
    
    print("\n" + "="*50)
    print("TESTING AGENTIC PLACE FINDER")
    print("="*50)
    
    for message in test_messages:
        response = await place_finder.chat(message)
        print("-" * 30)
        
    print("\n✅ Testing completed!")

if __name__ == "__main__":
    asyncio.run(main())
