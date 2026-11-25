
from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOLS, FUNCTION_NAME_TO_FUNCTION_MAP
import json
import os

load_dotenv()

client = OpenAI(
    base_url=os.getenv("BASE_URL"),
    api_key=os.getenv("API_KEY")
)

# Store conversation history
messages = []
## Safety limit: the max number of model rounds for one user question.
MAX_STEPS =5
messages.append(
    {
        "role" : "system",
        "content" : "aAct like a humble person and respond always under 50 words."
    }
)

while True:

    user_input = input("\nRahul: ")

    if user_input.lower() in ["exit", "quit", "bye", "goodbye"]:
        print("Assistant: Goodbye!")
        break

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
           
          ## print("Assistant (raw): "+ str(response))
        msg= response.choices[0].message
        if not msg.tool_calls:
            break
        messages.append(msg)

        for tool_call in msg.tool_calls:
            func_name = tool_call.function.name

            func_args = {}
            try:
                func_args= json.loads(tool_call.function.arguments or "{}")

                fn= FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
                result =fn(**func_args)
            except Exception as e:
                result = f"Error executing tool '{func_name}': {e}"
            messages.append({
                "role" : "tool",
                "tool_id" : tool_call.id,
                "content" : str(result),
            })
    else:
      # Ran out of steps. The model never gave the final answer?

        fallback = "Sorry, I couldnot finish this within the step limit."
        messages.append({
            "role" : "assistant",
            "content" : "fallback"
        })
        print("Assistant: " + fallback)
        continue
    
        messages.append({
        "role" : "assistant",
        "content" : msg.content

    })

    print("Assistant: " + msg.content)