# Multi-Agent Chat Application

A sophisticated chat application built with Google's Agent Development Kit (ADK) that implements a supervisor/sub-agent architecture using the Coordinator/Dispatcher pattern.

## Architecture

### Supervisor Agent
- **Main Coordinator**: Routes conversations to appropriate specialized sub-agents
- **LLM-Driven Delegation**: Uses Gemini-2.5-Flash to intelligently determine routing
- **Dynamic Routing**: Analyzes user intent and transfers to the best specialist

### Sub-Agents

1. **General Chat Agent** (`general_chat_agent`)
   - Handles casual conversation, greetings, and friendly interactions
   - Tools: `casual_chat_tool` for engaging conversation responses

2. **Task Manager Agent** (`task_manager_agent`)
   - Manages productivity, task creation, scheduling, and reminders
   - Tools: `create_task_tool`, `schedule_reminder_tool`

3. **Information Lookup Agent** (`info_lookup_agent`)
   - Provides factual information, research assistance, and fact-checking
   - Tools: `lookup_information_tool`, `fact_check_tool`

4. **Creative Writer Agent** (`creative_writer_agent`)
   - Assists with storytelling, creative writing, and content generation
   - Tools: `generate_story_tool`, `writing_prompt_tool`

## Deployment

### Prerequisites
- Google API Key configured in `.env` file
- ADK installed and configured

### Running the Application

```bash
# Navigate to the application directory
cd multi-agent-chat-app

# Start ADK Web server in debug mode
export GOOGLE_API_KEY="your_api_key_here"
adk web -v agents
```

### Testing Conversation Flows

1. **Casual Chat**: "Hello, how are you today?"
   - Routes to: `general_chat_agent`

2. **Task Management**: "Help me create a task for tomorrow"
   - Routes to: `task_manager_agent`

3. **Information Lookup**: "What do you know about quantum physics?"
   - Routes to: `info_lookup_agent`

4. **Creative Writing**: "Write me a short story about dragons"
   - Routes to: `creative_writer_agent`

## Features

- **Multi-Agent Coordination**: Supervisor intelligently routes conversations
- **Specialized Capabilities**: Each sub-agent has focused expertise and custom tools
- **Debug Mode**: Full visibility into agent transfers and decision-making
- **Session Management**: Maintains conversation state across agent transfers
- **LLM-Driven Intelligence**: Uses Gemini-2.5-Flash for natural language understanding

## Implementation Details

- **Framework**: Google Agent Development Kit (ADK)
- **Language Model**: Gemini-2.5-Flash
- **Pattern**: Coordinator/Dispatcher with LLM-Driven Delegation
- **Agent Hierarchy**: Supervisor with 4 specialized sub-agents
- **Communication**: ADK's built-in session state and agent transfer mechanisms
