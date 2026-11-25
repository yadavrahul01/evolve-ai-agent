
from datetime import datetime
import requests


# Function 1: Get current time
def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# Function 2: Get weather
def get_weather(city):
    try:
        url = f"https://wttr.in/{city}?format=3"

        response = requests.get(url, timeout=10)

        response.raise_for_status()

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
                "properties": {},
                "required": []
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
## print("Assistant (raw): "+ str(response))