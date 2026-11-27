
# ==========================================
# tool.py
# Sample tool for streaming experiments
# ==========================================

import json


# Function that performs addition
def add_numbers(a, b):

    return a + b


# Tool definition for the LLM
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_numbers",
            "description": "Add two numbers together.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number",
                        "description": "Second number"
                    }
                },
                "required": ["a", "b"]
            }
        }
    }
]


# Execute the requested tool
def run_tool(tool_name, arguments):

    if tool_name == "add_numbers":

        # Convert JSON arguments into Python dictionary
        args = json.loads(arguments)

        # Execute calculator
        result = add_numbers(
            args["a"],
            args["b"]
        )

        return result

    return "Tool not found"
