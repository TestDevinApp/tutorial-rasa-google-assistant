"""
Configuration for Agentic Place Finder
"""

import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "YOUR_GOOGLE_API_KEY")
MODEL_NAME = "gemini-2.0-flash-exp"
APP_NAME = "agentic_place_finder"
HOST = "0.0.0.0"
PORT = 8000

if GOOGLE_API_KEY == "YOUR_GOOGLE_API_KEY":
    print("⚠️  Warning: Please set your GOOGLE_API_KEY environment variable")
    print("   Get your key from: https://aistudio.google.com/app/apikey")

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"
