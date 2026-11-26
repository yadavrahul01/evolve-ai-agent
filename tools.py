
from datetime import datetime
from Utilities.utilities import log
import requests
import json


# Function 1: Get current time
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Function 2: Get weather
def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=3"

        response = requests.get(url, timeout=10)

        response.raise_for_status()  #This will raise the HTTP error if something goes wrong with the request.

        return response.text

    except requests.exceptions.RequestException as e:
        return f"Unable to fetch weather: {e}"

def get_user_city():
    return "Bangalore"
# Tool definitions
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Returns the current date and time.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Returns the current weather of a given city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "Name of the city to get weather for."
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_user_city",
            "description": "Returns the city where user lives. use this when user says 'my city' , 'where i live' or 'my location' without naming the city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city" : {
                        "type": "string",
                        "description": "Name of the city where user lives.",
                    }
                },
                "required": ["city"]
            } 
        }      
    }
]


# Function mapping
FUNCTION_NAME_TO_FUNCTION_MAP = {
    "get_current_time": get_current_time,
    "get_weather": get_weather,
     "get_user_city": get_user_city

}

def run_tool(tool_call):
     func_name = tool_call.function.name
    
     func_args = {}
     try:
         func_args= json.loads(tool_call.function.arguments or "{}")
         log(f"Calling function {func_name} with arguements {func_args}")
         fn= FUNCTION_NAME_TO_FUNCTION_MAP[func_name]
         result =fn(**func_args)
     except Exception as e:
         result = f"Error executing tool '{func_name}': {e}"
     log(f"  {result}")
     result = str(result)