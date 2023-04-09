import speech_recognition as sr
import openai
import time
import config
import api_keys
import translator
import random
import json
import threading
import re
from playsound import playsound
import requests

from twitch_chat_irc import twitch_chat_irc


# https://pypi.org/project/twitch-chat-irc/
# https://platform.openai.com/account/api-keys

# TODO
# https://github.com/lacson/webcaptioner-stream распознование звука
from generate_text import generate_text


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


def send_message(_message):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    _message = emoji_pattern.sub(r'', _message)
    if "[ERROR]" not in _message:
        connection = twitch_chat_irc.TwitchChatIRC('NeoBasedAI', api_keys.twitch)
        connection.send(config.streamer, _message)
        connection.close_connection()




def add_tag(_message):
    uList = ["ты", "тебя", "тебе", "твои", "твой", "тобой"]
    randomNumber = random.randint(0, 17)

    for word in uList:
        if word in _message:
            return "@" + config.streamer + " " + _message

    if randomNumber == 1:
        return "@" + config.streamer + " " + _message
    else:
        return _message


def add_emojis(_message):
    showEmoji = random.randint(0, 1)
    if showEmoji == 1:
        emojiNumber = random.randint(0, len(config.emojis) - 1)
        amount = random.randint(1, 3)
        return _message + " " + ((config.emojis[emojiNumber] + " ") * amount)
    else:
        return _message


def say(_message):
    url = 'https://tts.voicetech.yandex.net/tts?&format=mp3&lang=ru_RU&speed=1.3&emotion=neutral&speaker=nick&robot=1&text=' + _message

    response = requests.get(url)

    # Check if the request was successful
    try:
        if response.status_code == 200:
            # Write the file to disk
            with open('file.mp3', 'wb') as f:
                f.write(response.content)
            print('File saved successfully.')

            # Play the file
            playsound('./file.mp3')
            print('File played successfully.')
        else:
            print('Error:', response.status_code)
    finally:
        print("bruh")

def remove_basic_emojis(_message):
    _message = _message.replace(":)", "").replace(";)", "").replace(":D", "")
    return _message


def remove_punctuation(_message):
    return _message.replace("!", "").replace(".", "")


def prettify(_message):
    _message = add_tag(_message)
    _message = add_emojis(_message)
    _message = remove_basic_emojis(_message)
    return _message


def audio_ai():
    openai.api_key = api_keys.openai
    r = sr.Recognizer()
    while True:
        message = ""
        with sr.Microphone() as source:
            print("[audio_ai]: " + "Listening")
            audio_text = r.listen(source, phrase_time_limit=10)
            print("[audio_ai]: " + "Recognising")

        try:
            recognisingResult = r.recognize_google(audio_text, language="ru-RU", show_all=True)
            transcript = recognisingResult['alternative'][0]['transcript']
            confidence = recognisingResult['alternative'][0]['confidence']
            print("[audio_ai]: " + str(confidence))
            print("[audio_ai]: " + bcolors.OKCYAN + transcript + bcolors.ENDC)

            message = generate_text(transcript)
            #else:
            #    print("[audio_ai]: " + "Small input")
        except Exception as e:
            print(e)

        if message != "":
            print("[audio_ai][second_response]: " + bcolors.OKGREEN + message + bcolors.ENDC)

            if config.stream_mode:
                say(message)
            else:
                send_message(prettify(message))
            sleep_time = random.randint(20, 45)
            print("[audio_ai]: " + "Sleeping for: " + str(sleep_time))
            if not config.FAST_SLEEP:
                time.sleep(sleep_time)


def handle_message(message):
    decoded_tag = message['display-name']
    decoded_message = message['message']
    if "@neobased" in str(decoded_message).lower() or "@neobasedai" in str(decoded_message).lower():
        print("[text_ai]: " + bcolors.OKGREEN + str(decoded_message) + bcolors.ENDC)


        ai_message = generate_text(decoded_message)
        pattern = re.compile(re.escape("@neobasedai"), re.IGNORECASE)
        ai_message = pattern.sub("", ai_message)
        if "@neobasedai" in decoded_tag:
            print("Пытались наебать")
        else:
            ai_message = "@" + decoded_tag + " " + ai_message
        ai_message = add_emojis(ai_message)
        print("[text_ai][second_response]: " + bcolors.OKGREEN + ai_message + bcolors.ENDC)
        if config.stream_mode:
            say(ai_message)
        else:
            send_message(ai_message)
    else:
        print("[text_ai]: " + bcolors.WARNING + str(decoded_message) + bcolors.ENDC)


def text_ai():
    connection = twitch_chat_irc.TwitchChatIRC('NeoBased', api_keys.twitch)
    connection.listen(config.streamer, on_message=handle_message)
    connection.close_connection()


if __name__ == "__main__":
    text_ai_thread = threading.Thread(target=text_ai, args=())
    text_ai_thread.start()
    if not config.stream_mode:
        audio_ai_thread = threading.Thread(target=audio_ai, args=())
        audio_ai_thread.start()


        #generate_text()
        #if len(transcript.split(" ")) >= 4:
        #response = openai.Completion.create(
        #    model="text-davinci-003",
        #    prompt="give a new short and funny answer to this message: \"" + transcript + "\"",
        #    temperature=0.75,
        #    max_tokens=256,
        #    top_p=1,
        #    best_of=1,
        #    frequency_penalty=0,
        #    presence_penalty=0
        #)
        #message = response["choices"][0]["text"].replace("\"", "").replace("\n", "")
        #message = message.replace("!", "")
        #print("[audio_ai][first_response]: " + bcolors.WARNING + message + bcolors.ENDC)
        #response = openai.Completion.create(
        #    model="text-davinci-003",
        #    prompt="вставь слово бля в случайное место в этом сообщении: \"" + message + "\"",
        #    temperature=0.7,
        #    max_tokens=256,
        #    top_p=1,
        #    best_of=1,
        #    frequency_penalty=0,
        #    presence_penalty=0
        #)
        #message = response["choices"][0]["text"].replace("\"", "").replace("\n", "")
        #message = message.replace("!", "")


        #response = openai.Completion.create(  # TODO рефактор генерации TODO похуй)
        #    model="text-davinci-003",
        #    prompt="give a new short and funny answer to this message: \"" + decoded_message + "\"",
        #    temperature=0.75,
        #    max_tokens=256,
        #    top_p=1,
        #    best_of=1,
        #    frequency_penalty=0,
        #    presence_penalty=0
        #)
        #ai_message = response["choices"][0]["text"].replace("\"", "").replace("\n", "")
        #ai_message = ai_message.replace("!", "")
        #print("[text_ai][first_response]: " + bcolors.WARNING + ai_message + bcolors.ENDC)
        #response = openai.Completion.create(
        #    model="text-davinci-003",
        #    prompt="вставь слово бля в случайное место в этом сообщении: \"" + ai_message + "\"",
        #    temperature=0.7,
        #    max_tokens=256,
        #    top_p=1,
        #    best_of=1,
        #    frequency_penalty=0,
        #    presence_penalty=0
        #)
        #ai_message = response["choices"][0]["text"].replace("\"", "").replace("\n", "").replace("!", "")