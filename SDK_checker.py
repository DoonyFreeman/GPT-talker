from google import genai
import os

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

models = client.models.list_models()
for m in models:
    print(m.name, m.supported_methods)