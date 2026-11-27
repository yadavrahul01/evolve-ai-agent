
# ==========================================
# test.py
# Testing normal LLM response
# ==========================================

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to local Ollama server
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

# Get model name from .env
MODEL = os.getenv("MODEL")

# Send a request to the model
response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "user",
            "content": "Explain what an AI agent is."
        }
    ]
)

# Extract completed response
answer = response.choices[0].message.content

# Display answer
print("\nAssistant:", answer)
