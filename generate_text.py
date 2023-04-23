import json
import os
import re

import requests
import api_keys
import config
from say import say


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
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_keys.bearer}",
    }

    data = {
        "prompt": config.prompt_base + _input_message,
        "models": [
            {
                "name": "openai:gpt-3.5-turbo", #3.5-turbo
                "tag": "openai:gpt-3.5-turbo",
                "provider": "openai",
                "parameters": {
                    "temperature": 0.99,
                    "maximumLength": 572,
                    "topP": 1,
                    "presencePenalty": 0.15,
                    "frequencyPenalty": 0.25,
                    "stopSequences": [

                    ]
                },
                "enabled": True,
                "selected": True
            }
        ]
    }

    session = requests.Session()
    response = session.post(api_keys.url, headers=headers, data=json.dumps(data), stream=True)
    if not config.DEBUG_MODE:
        os.system('cls')
    print("[audio_ai]: " + bcolors.OKGREEN + "============================ Я ДУМАЮ НАД ОТВЕТОМ =============================" + bcolors.ENDC)
    BIG_text = ""
    text_line = ""
    for line in response.iter_lines(decode_unicode=True):
        if line:
            if "data" in line:
                decoded_line = json.loads(line[5:])['message']  # приходит какое то говно, убираем "data:"
                if decoded_line != "[INITIALIZING]":
                    if "." in decoded_line or "!" in decoded_line or "?" in decoded_line or ":" in decoded_line:
                        text_line += decoded_line
                        if config.DIALOG_MODE:
                            say(text_line)
                        BIG_text += text_line
                        print(text_line)
                        text_line = ""
                    else:
                        text_line += decoded_line
    return BIG_text


# TODO шиза и вместо регулярки надо вытаскивать из json просто, какой ебалан это писал?
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

    """if line != "event:status":
        decoded_line = json.loads(line)["data"]["message"]
        print("DECODED: " + decoded_line)
    
    if line:
        if "." or "!" or "?" in line:
            text_line += line
            #say(text_line)
            BIG_text += text_line
            print("SENTENCE: " + BIG_text)
            text_line = ""
        else:
            text_line += line
        # Do something with the event data; for example, print it
        print(f"Event data: {line}")"""

# print(text_line)
# return text_line
# if response.status_code == 200:
#    print("[RECEIVED")
#    text = extract_text(response.content)
#    print("[text_ai]" + bcolors.OKGREEN + text + bcolors.ENDC)
#    return text
# else:
#    print(f"Request failed with status code {response.status_code}.")
#    return ""
