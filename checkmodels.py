import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load your Google API key from .env
load_dotenv()

# Configure Gemini client
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# List all available models
print("📋 Available Gemini Models:\n")
for model in genai.list_models():
    print(f"- {model.name}  |  Supported methods: {model.supported_generation_methods}")
