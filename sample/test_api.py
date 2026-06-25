import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

print("API Key Found:", bool(api_key))

genai.configure(api_key=api_key)

# List all available models
for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(model.name)
        