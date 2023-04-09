import json
import re

import requests
import api_keys
import config


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def generate_text(_input_message):
    url = "https://nat.dev/api/stream"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_keys.bearer}"
    }

    data = {
        "prompt": config.prompt_base + _input_message,
        "models": [
            {
                "name": "openai:gpt-4",
                "tag": "openai:gpt-4",
                "provider": "openai",
                "parameters": {
                    "temperature": 0.69,
                    "maximumLength": 572,
                    "topP": 1,
                    "presencePenalty": 0,
                    "frequencyPenalty": 0,
                    "stopSequences": [

                    ]
                },
                "enabled": True,
                "selected": True
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        text = extract_text(response.content)
        print("[text_ai]" + bcolors.OKGREEN + text + bcolors.ENDC)
        return text
    else:
        print(f"Request failed with status code {response.status_code}.")
        return ""


def extract_text(_bullshit_input):
    messages = []
    pattern = r'data:{"message": "(.*?)",'
    decoded_string = _bullshit_input.decode('utf-8')
    for match in re.finditer(pattern, decoded_string):
        message = match.group(1)
        messages.append(message)

    combined_text = "".join(messages)
    decoded_text = bytes(combined_text, "utf-8").decode("unicode_escape")
    decoded_text = decoded_text.replace("[INITIALIZING]", "").replace("[COMPLETED]", "")
    return decoded_text


if __name__ == "__main__":
    generate_text("Ты любишь негров?")
