import re
import time
import random
import threading

import speech_recognition as sr
import openai
from playsound import playsound
import requests
from twitch_chat_irc import twitch_chat_irc
from generate_text import generate_text

import config
import api_keys
from colors import Color


# TODO
# https://github.com/lacson/webcaptioner-stream распознование звука
U_LIST = set(["ты", "тебя", "тебе", "твои", "твой", "тобой"])


def send_message(message: str):
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "]+",
        flags=re.UNICODE,
    )
    message = emoji_pattern.sub(r"", message)
    if "[ERROR]" not in message:
        connection = twitch_chat_irc.TwitchChatIRC("NeoBasedAI", api_keys.twitch)
        connection.send(config.streamer, message)
        connection.close_connection()


def add_tag(message):
    randomNumber = random.randint(0, 17)

    for word in U_LIST:
        if word in message:
            return "@" + config.streamer + " " + message

    if randomNumber == 1:
        return "@" + config.streamer + " " + message

    return message


def add_emojis(message):
    showEmoji = random.randint(0, 1)
    if showEmoji == 1:
        emojiNumber = random.randint(0, len(config.emojis) - 1)
        amount = random.randint(1, 3)
        return message + " " + ((config.emojis[emojiNumber] + " ") * amount)
    return message


def say(_message):
    url = (
        "https://tts.voicetech.yandex.net/tts?&format=mp3&lang=ru_RU&speed=1.3&emotion=neutral&speaker=nick&robot=1&text="
        + _message
    )

    response = requests.get(url)

    # Check if the request was successful
    try:
        if response.status_code == 200:
            # Write the file to disk
            with open("file.mp3", "wb") as f:
                f.write(response.content)
            print("File saved successfully.")

            # Play the file
            playsound("./file.mp3")
            print("File played successfully.")
        else:
            print("Error:", response.status_code)
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
            recognisingResult = r.recognize_google(
                audio_text, language="ru-RU", show_all=True
            )
            transcript = recognisingResult["alternative"][0]["transcript"]
            confidence = recognisingResult["alternative"][0]["confidence"]
            print("[audio_ai]: " + str(confidence))
            print("[audio_ai]: " + Color.OKCYAN + transcript + Color.ENDC)

            message = generate_text(transcript)
        except Exception as e:
            print(e)

        if message != "":
            print(
                "[audio_ai][second_response]: " + Color.OKGREEN + message + Color.ENDC
            )

            if config.stream_mode:
                say(message)
            else:
                send_message(prettify(message))
            sleep_time = random.randint(20, 45)
            print(f"[audio_ai]: Sleeping for: {sleep_time}")
            if not config.FAST_SLEEP:
                time.sleep(sleep_time)


def handle_message(message):
    decoded_tag = message["display-name"]
    decoded_message = message["message"]
    if (
        "@neobased" in str(decoded_message).lower()
        or "@neobasedai" in str(decoded_message).lower()
    ):
        print("[text_ai]: " + Color.OKGREEN + str(decoded_message) + Color.ENDC)

        ai_message = generate_text(decoded_message)
        pattern = re.compile(re.escape("@neobasedai"), re.IGNORECASE)
        ai_message = pattern.sub("", ai_message)
        if "@neobasedai" in decoded_tag:
            print("Пытались наебать")
        else:
            ai_message = "@" + decoded_tag + " " + ai_message
        ai_message = add_emojis(ai_message)
        print("[text_ai][second_response]: {Color.OKGREEN} {ai_message} {Color.ENDC}")
        if config.stream_mode:
            say(ai_message)
        else:
            send_message(ai_message)
    else:
        print(f"[text_ai]: {Color.WARNING} {decoded_message} {Color.ENDC}")


def text_ai():
    connection = twitch_chat_irc.TwitchChatIRC("NeoBased", api_keys.twitch)
    connection.listen(config.streamer, on_message=handle_message)
    connection.close_connection()


if __name__ == "__main__":
    text_ai_thread = threading.Thread(target=text_ai, args=())
    text_ai_thread.start()
    if not config.stream_mode:
        audio_ai_thread = threading.Thread(target=audio_ai, args=())
        audio_ai_thread.start()
