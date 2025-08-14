"""
Details Agent for Place Finder Multi-Agent System
Provides specific details about places like address, rating, and opening hours
"""

from google.adk.agents import Agent

def get_place_details_tool(detail_type: str, context: str = "") -> str:
    """
    Provides specific details about a place based on the type requested.
    
    Args:
        detail_type (str): Type of detail requested ("address", "rating", "opening_hours")
        context (str): Context about the place from previous conversation
        
    Returns:
        str: The requested detail information
    """
    print(f"--- Tool: get_place_details_tool called for {detail_type} ---")
    
    if detail_type == "address":
        return "The address is 123 Main Street, Downtown. It's about a 5-minute walk from your current location."
    elif detail_type == "rating":
        return "This place has a rating of 4.5 out of 5 stars based on 127 customer reviews. Customers particularly praise the quality and service."
    elif detail_type == "opening_hours":
        return "The place is currently open. Opening hours are 11:00 AM to 10:00 PM, Monday through Sunday. They're closed on major holidays."
    else:
        return f"I can provide information about {detail_type}. Please specify if you'd like the address, rating, or opening hours for the place we discussed."

root_agent = Agent(
    name="details_agent", 
    model="gemini-2.0-flash-exp",
    description="Provides specific details about places like address, rating, and opening hours",
    instruction="You provide specific details about places that were found in previous searches. Use get_place_details_tool when users ask for address, rating, or opening hours. Extract the detail type from the user's question and provide helpful, specific information.",
    tools=[get_place_details_tool]
)
