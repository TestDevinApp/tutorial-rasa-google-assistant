"""
Place Search Agent for Agentic Place Finder
Main agent that handles place searches and weather queries
"""

from google.adk.agents import Agent

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

root_agent = Agent(
    name="place_search_agent",
    model="gemini-2.0-flash-exp",
    description="Main agent that handles place searches and weather queries",
    instruction="""You are the main Place Finder agent. Your responsibilities:

1. For place searches: Use 'get_weather_with_location' tool with the place type as 'city' and extract radius from user input (default 100m if not specified)
2. When users ask "I am looking for a [PLACE] within [NUMBER] meters", extract:
- PLACE as the city parameter
- NUMBER as the radius parameter

Present search results clearly, mentioning the place found, weather conditions, and ask if they need more details.""",
    tools=[get_weather_with_location]
)
