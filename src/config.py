import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
weather_api_key = os.getenv("weather_api_key")

# Model Configuration
MODEL_NAME = "gemini-2.5-flash"

# App Configuration
APP_TITLE = "FarmAssist - For Nigerian Farmers"
APP_ICON = "🌿"
