"""
ADK Web deployment for Agentic Place Finder
"""

import os
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import uvicorn
from place_finder_agent.agent import AgenticPlaceFinder
import config

app = FastAPI(title="Agentic Place Finder", description="ADK-powered place search chatbot")

place_finder = None

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@app.on_event("startup")
async def startup_event():
    """Initialize the agentic place finder on startup"""
    global place_finder
    
    if not os.environ.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_KEY") == "YOUR_GOOGLE_API_KEY":
        print("⚠️  Warning: GOOGLE_API_KEY not set. Using mock responses.")
    
    place_finder = AgenticPlaceFinder()
    await place_finder.initialize()
    print("✅ Agentic Place Finder initialized and ready!")

@app.get("/", response_class=HTMLResponse)
async def get_chat_interface():
    """Serve the chat interface"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Agentic Place Finder</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .chat-container { border: 1px solid #ddd; height: 400px; overflow-y: auto; padding: 10px; margin-bottom: 10px; }
            .message { margin: 10px 0; padding: 8px; border-radius: 5px; }
            .user { background-color: #e3f2fd; text-align: right; }
            .assistant { background-color: #f5f5f5; }
            .input-container { display: flex; gap: 10px; }
            input[type="text"] { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
            button { padding: 10px 20px; background-color: #2196f3; color: white; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background-color: #1976d2; }
            .header { text-align: center; color: #333; margin-bottom: 20px; }
            .examples { background-color: #f9f9f9; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
            .examples h3 { margin-top: 0; }
            .example { cursor: pointer; color: #2196f3; margin: 5px 0; }
            .example:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🤖 Agentic Place Finder</h1>
            <p>Powered by Google ADK & Gemini-2.5-Flash</p>
        </div>
        
        <div class="examples">
            <h3>Try these examples:</h3>
            <div class="example" onclick="sendExample('Hello')">👋 Hello</div>
            <div class="example" onclick="sendExample('I am looking for a restaurant within 50 meters')">🍽️ I am looking for a restaurant within 50 meters</div>
            <div class="example" onclick="sendExample('What is the address?')">📍 What is the address?</div>
            <div class="example" onclick="sendExample('What is the rating?')">⭐ What is the rating?</div>
            <div class="example" onclick="sendExample('Is it open now?')">🕐 Is it open now?</div>
            <div class="example" onclick="sendExample('I need a bank within 200 meters')">🏦 I need a bank within 200 meters</div>
            <div class="example" onclick="sendExample('Goodbye')">👋 Goodbye</div>
        </div>
        
        <div class="chat-container" id="chatContainer">
            <div class="message assistant">
                <strong>Assistant:</strong> Hello! I'm your Agentic Place Finder assistant. I can help you find places and check weather information. What are you looking for?
            </div>
        </div>
        
        <div class="input-container">
            <input type="text" id="messageInput" placeholder="Type your message here..." onkeypress="handleKeyPress(event)">
            <button onclick="sendMessage()">Send</button>
        </div>

        <script>
            async function sendMessage() {
                const input = document.getElementById('messageInput');
                const message = input.value.trim();
                if (!message) return;

                const chatContainer = document.getElementById('chatContainer');
                
                // Add user message
                const userDiv = document.createElement('div');
                userDiv.className = 'message user';
                userDiv.innerHTML = '<strong>You:</strong> ' + message;
                chatContainer.appendChild(userDiv);
                
                // Clear input
                input.value = '';
                
                // Scroll to bottom
                chatContainer.scrollTop = chatContainer.scrollHeight;
                
                try {
                    // Use absolute URL to avoid credentials issue
                    const baseUrl = window.location.protocol + '//' + window.location.host;
                    const response = await fetch(baseUrl + '/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ message: message })
                    });
                    
                    const data = await response.json();
                    
                    // Add assistant response
                    const assistantDiv = document.createElement('div');
                    assistantDiv.className = 'message assistant';
                    assistantDiv.innerHTML = '<strong>Assistant:</strong> ' + data.response;
                    chatContainer.appendChild(assistantDiv);
                    
                } catch (error) {
                    const errorDiv = document.createElement('div');
                    errorDiv.className = 'message assistant';
                    errorDiv.innerHTML = '<strong>Assistant:</strong> Sorry, I encountered an error: ' + error.message;
                    chatContainer.appendChild(errorDiv);
                }
                
                // Scroll to bottom
                chatContainer.scrollTop = chatContainer.scrollHeight;
            }
            
            function sendExample(message) {
                document.getElementById('messageInput').value = message;
                sendMessage();
            }
            
            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(chat_message: ChatMessage):
    """Handle chat messages"""
    global place_finder
    
    if not place_finder:
        raise HTTPException(status_code=500, detail="Place finder not initialized")
    
    try:
        response = await place_finder.chat(chat_message.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Agentic Place Finder"}

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=config.HOST,
        port=config.PORT,
        reload=True
    )
