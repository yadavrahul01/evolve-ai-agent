
# standard libraary imports
import os

# third party imports
from openai import OpenAI
from dotenv import load_dotenv

# local modules
from tools import TOOLS, run_tool
from Utilities.utilities import log


load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

# Store conversation history
messages = []

## Safety limit: the max number of model rounds for one user question.
MAX_STEPS = 5

messages.append(
    {
        "role": "system",
        "content": (
            "You are a helpful humble assistant."
            " Answer general questions (programming, science, advice) from your own knowledge."
            " Use a tool only when the user asks for current time or weather or their city."
            " Keep the words under 100 words."
        ),
    }
)

while True:

    user_input = input("\nRahul: ").strip()

    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        print("Assistant: Goodbye!")
        break

    # Ignore empty input
    if not user_input:
        continue

    # Add user message
    messages.append({
        "role": "user",
        "content": user_input
    })

    ## Chained Tool calling

    for step in range(MAX_STEPS):

        response = client.chat.completions.create(
            model=os.getenv("MODEL"),
            messages=messages,
            tools=TOOLS,
        )

        ## print("Assistant (raw): " + str(response))

        msg = response.choices[0].message

        # Check whether the model requested any tool calls
        if not msg.tool_calls:
            break

        log(f"Step {step+1}: model requested {len(msg.tool_calls)} tool calls.")

        # Store assistant tool-call message
        messages.append(msg)

        for tool_call in msg.tool_calls:

            # Execute the requested tool
            result = run_tool(tool_call)

            # Store tool response
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result),
            })

    else:
        # Ran out of steps. The model never gave the final answer?

        fallback = "Sorry, I could not finish this within the step limit."

        messages.append({
            "role": "assistant",
            "content": fallback
        })

        print("Assistant: " + fallback)
        continue

    # Store final assistant response
    messages.append({
        "role": "assistant",
        "content": msg.content or ""
    })

    # Display final response
    print("Assistant: " + (msg.content or ""))
