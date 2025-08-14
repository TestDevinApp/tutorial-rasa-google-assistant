"""
Place Search Agent for Place Finder Multi-Agent System
Handles place searches and location queries with mock Google Places API functionality
"""

from google.adk.agents import Agent

def search_places_tool(query: str, radius: str = "100") -> dict:
    """
    Searches for places based on query and radius using mock Google Places API.
    
    Args:
        query (str): The type of place to search for (e.g., "restaurant", "cafe", "shop")
        radius (str): Search radius in meters (default: "100")
    
    Returns:
        dict: Place information with status, name, rating, address, and opening_hours
    """
    print(f"--- Tool: search_places_tool called for query: {query}, radius: {radius}m ---")
    
    query_normalized = query.lower().replace(" ", "")
    
    mock_places_db = {
        "restaurant": {
            "status": "success",
            "name": "The Downtown Bistro",
            "report": f"Found a highly-rated restaurant within {radius}m radius. Great for dining!",
            "rating": "4.5",
            "address": "123 Main Street, Downtown",
            "opening_hours": "11:00 AM - 10:00 PM, Monday through Sunday"
        },
        "cafe": {
            "status": "success",
            "name": "Coffee Corner",
            "report": f"Found a cozy cafe within {radius}m radius. Perfect for coffee and snacks!",
            "rating": "4.2",
            "address": "456 Oak Avenue, City Center", 
            "opening_hours": "7:00 AM - 8:00 PM, Daily"
        },
        "shop": {
            "status": "success",
            "name": "City Mall",
            "report": f"Found a shopping center within {radius}m radius. Great for shopping!",
            "rating": "4.0",
            "address": "789 Commerce Street, Shopping District",
            "opening_hours": "10:00 AM - 9:00 PM, Monday through Saturday"
        },
        "bank": {
            "status": "success", 
            "name": "First National Bank",
            "report": f"Found a bank within {radius}m radius. Full banking services available!",
            "rating": "3.8",
            "address": "321 Financial Plaza, Business District",
            "opening_hours": "9:00 AM - 5:00 PM, Monday through Friday"
        }
    }
    
    if query_normalized in mock_places_db:
        return mock_places_db[query_normalized]
    else:
        return {
            "status": "error",
            "error_message": f"Sorry, I couldn't find any {query} within {radius}m radius. Try searching for restaurants, cafes, shops, or banks.",
            "rating": None,
            "address": None,
            "opening_hours": None
        }

root_agent = Agent(
    name="place_search_agent",
    model="gemini-2.0-flash-exp",
    description="Handles place searches and location queries with Google Places API integration", 
    instruction="""You are a place search specialist. When users ask "I am looking for a [PLACE] within [NUMBER] meters", extract:
- PLACE as the query parameter
- NUMBER as the radius parameter (default 100m if not specified)

Use search_places_tool to find places and present results clearly, mentioning the place found, rating, and ask if they need more details like address or opening hours.""",
    tools=[search_places_tool]
)
