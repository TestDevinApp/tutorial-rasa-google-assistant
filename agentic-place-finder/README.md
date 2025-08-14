# Agentic Place Finder

An agentic AI application that replicates the functionality of the Rasa place finder chatbot using Google ADK framework and Gemini-2.5-Flash model.

## Overview

This application demonstrates how to convert a traditional Rasa NLP chatbot into an agentic AI system using Google's Agent Development Kit (ADK). It maintains the same conversation flows and functionality while leveraging modern agentic architecture patterns.

## Features

- **Multi-Agent Architecture**: Specialized agents for greetings, place search, details, and farewells
- **Intent Recognition**: Handles greet, place_search, opening_hours, address, rating, goodbye, thanks, inform intents
- **Entity Extraction**: Extracts place types (query) and search radius (number) from user input
- **Place Search**: Mock Google Places API integration for location searches
- **Conversation State**: Session management across multiple agents
- **Web Interface**: Browser-based chat interface using ADK Web

## Agent Architecture

### Main Agent (place_search_agent)
- Coordinates conversation flow
- Handles place searches using `get_weather_with_location` tool
- Delegates to specialized sub-agents based on user intent

### Sub-Agents
- **Greeting Agent**: Handles welcome messages
- **Farewell Agent**: Manages goodbye interactions  
- **Details Agent**: Provides specific place information (address, rating, hours)

## Installation

1. **Clone and navigate to the project:**
```bash
cd agentic-place-finder
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env and add your Google API key
```

4. **Get Google API Key:**
- Visit: https://aistudio.google.com/app/apikey
- Create a new API key
- Add it to your `.env` file

## Usage

### Command Line Testing
```bash
python place_finder_agent/agent.py
```

### Web Interface
```bash
python app.py
```
Then open: http://localhost:8000

### Example Conversations

**Place Search:**
```
User: I am looking for a restaurant within 50 meters
Assistant: Found a highly-rated restaurant within 50m radius. Current weather conditions are favorable. Rating: 4.3/5. Would you like more details?

User: What's the address?
Assistant: The address is 123 Main Street, Downtown. It's about a 5-minute walk from here.

User: What's the rating?
Assistant: This place has a rating of 4.5 out of 5 stars based on customer reviews.
```

## Comparison with Original Rasa Chatbot

| Feature | Rasa Implementation | Agentic Implementation |
|---------|-------------------|----------------------|
| Intent Classification | NLU pipeline with training data | Gemini-2.5-Flash with prompt engineering |
| Entity Extraction | CRF + spaCy | LLM-based extraction in prompts |
| Dialogue Management | Stories + policies | Agent delegation patterns |
| Action Execution | Custom actions with slots | Tool functions with session state |
| API Integration | Python requests in actions | Tool functions with structured responses |
| Deployment | Rasa server + action server | FastAPI + ADK Web |

## Project Structure

```
agentic-place-finder/
├── place_finder_agent/
│   ├── __init__.py
│   └── agent.py          # Main agent implementation
├── app.py                # ADK Web deployment
├── config.py             # Configuration settings
├── requirements.txt      # Dependencies
├── .env.example         # Environment template
└── README.md            # This file
```

## Tools and Functions

### get_weather_with_location(city, radius)
Mock implementation of Google Places API integration that returns structured place data including status, report, rating, address, and opening hours.

### get_place_details(detail_type, context)
Provides specific information about places based on the requested detail type (address, rating, opening_hours).

### say_hello() / say_goodbye()
Handle greeting and farewell interactions with appropriate responses.

## Development

The application uses mock data for place searches to avoid requiring actual Google API keys during development. In production, replace the mock functions with real Google Places API calls.

## Deployment

The application can be deployed using:
- Local development server (uvicorn)
- Docker containers
- Cloud platforms supporting FastAPI applications
- ADK Web deployment patterns

## License

This project replicates the functionality of the original Rasa tutorial for educational purposes.
