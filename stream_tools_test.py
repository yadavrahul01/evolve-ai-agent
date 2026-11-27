
# ==========================================
# stream_tools_test.py
# Streaming + Tool Calling
# ==========================================

import os
import json

from openai import OpenAI
from dotenv import load_dotenv

from tool import TOOLS, run_tool


# Load environment variables
load_dotenv()

# Connect to Ollama
client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

MODEL = os.getenv("MODEL")

MAX_STEPS = 5


# Conversation history
messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant. Use the calculator tool for arithmetic."
    },
    {
        "role": "user",
        "content": "Calculate 25 + 75 using the calculator tool."
    }
]


# ==========================================
# Function to receive streamed responses
# ==========================================

def stream_response(messages):

    # Request streamed completion
    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=TOOLS,
        stream=True
    )

    # Store generated text
    assistant_text = ""

    # Store streamed tool calls
    tool_calls = {}

    print("\nAssistant: ", end="", flush=True)

    # Receive chunks
    for chunk in stream:

        delta = chunk.choices[0].delta

        # ----------------------------------
        # Collect normal text chunks
        # ----------------------------------

        if delta.content:

            assistant_text += delta.content

            print(
                delta.content,
                end="",
                flush=True
            )

        # ----------------------------------
        # Collect tool call chunks
        # ----------------------------------

        if delta.tool_calls:

            for tool_delta in delta.tool_calls:

                index = tool_delta.index

                # Initialize tool call storage
                if index not in tool_calls:

                    tool_calls[index] = {
                        "id": "",
                        "type": "function",
                        "function": {
                            "name": "",
                            "arguments": ""
                        }
                    }

                current = tool_calls[index]

                # Collect tool ID
                if tool_delta.id:
                    current["id"] = tool_delta.id

                # Collect function details
                if tool_delta.function:

                    if tool_delta.function.name:

                        current["function"]["name"] += (
                            tool_delta.function.name
                        )

                    if tool_delta.function.arguments:

                        current["function"]["arguments"] += (
                            tool_delta.function.arguments
                        )

    print()

    # Return collected response
    return assistant_text, tool_calls


# ==========================================
# Main chained tool calling loop
# ==========================================

for step in range(MAX_STEPS):

    print(f"\n--- Model Round {step + 1} ---")

    assistant_text, tool_calls = stream_response(messages)

    # --------------------------------------
    # No tool calls: final response received
    # --------------------------------------

    if not tool_calls:

        messages.append({
            "role": "assistant",
            "content": assistant_text
        })

        break

    # --------------------------------------
    # Store assistant tool call message
    # --------------------------------------

    ordered_calls = [
        tool_calls[index]
        for index in sorted(tool_calls)
    ]

    messages.append({
        "role": "assistant",
        "content": assistant_text or None,
        "tool_calls": ordered_calls
    })

    # --------------------------------------
    # Execute requested tools
    # --------------------------------------

    for call in ordered_calls:

        tool_name = call["function"]["name"]

        arguments = call["function"]["arguments"]

        print(f"\nExecuting tool: {tool_name}")

        try:

            result = run_tool(
                tool_name,
                arguments
            )

        except Exception as error:

            result = f"Tool execution failed: {error}"

        print("Tool result:", result)

        # Send tool result back to model
        messages.append({
            "role": "tool",
            "tool_call_id": call["id"],
            "content": str(result)
        })

else:

    print("\nMaximum tool-call steps reached.")

