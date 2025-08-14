"""
Details Agent for Agentic Place Finder
Provides specific details about places like address, rating, and opening hours
"""

from google.adk.agents import Agent

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

root_agent = Agent(
    name="place_details_agent", 
    model="gemini-2.0-flash-exp",
    description="Provides specific details about places like address, rating, and opening hours",
    instruction="You provide specific details about places. Use 'get_place_details' tool when users ask for address, rating, or opening hours. Extract the detail type from the user's question.",
    tools=[get_place_details]
)
