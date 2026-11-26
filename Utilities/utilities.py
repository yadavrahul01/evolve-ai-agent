import os
START_SEQUENCE = "\033[90M"  ## ANSI escape code for every grey text
END_SEQUENCE = "\033[0M"     ##  ANSI escape codeto reset text color

def log(text):
    if os.getenv("DEBUG") == "True":
        print(f"{START_SEQUENCE}{text}{END_SEQUENCE}")