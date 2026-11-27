
# ==========================================
# stream_test.py
# Basic LLM text streaming
# ==========================================

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to Ollama
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

MODEL = os.getenv("MODEL")

# Conversation messages
messages = [
    {
        "role": "system",
        "content": "You are a helpful AI assistant."
    },
    {
        "role": "user",
        "content": "Explain how neural networks work."
    }
]

# Request streaming response
stream = client.chat.completions.create(
    model=MODEL,
    messages=messages,
    stream=True
)

print("\nAssistant: ", end="", flush=True)

# Receive chunks one by one
for chunk in stream:

    # Extract newly generated content
    content = chunk.choices[0].delta.content

    # Display content immediately
    if content:
        print(content, end="", flush=True)

print("\n")
