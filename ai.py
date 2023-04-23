import os
from asyncio import Queue

import speech_recognition as sr
# import openai
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


#                        MADE BY NEODIM
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠐⠂⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⡠⠴⠤⣤⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⢀⣀⣀⣀⣀⡀⠀⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠀⠈⠉⢁⣈⣿⣿⣿⣷⡀⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠃⠠⠴⠒⠛⠛⠛⠛⠛⠛⠛⠷⠄⠘⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⠀⣀⣤⣴⣶⣶⣶⣶⣶⣶⣤⣄⣀⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⣠⣾⣿⠿⠟⠛⠛⠛⠛⠛⠿⠿⣿⣿⣷⣆⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠀⠐⠋⠉⣀⡠⠤⠔⠒⠒⠒⠠⠤⢀⡀⠉⠛⠿⣆⠀⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⢀⣠⠔⠊⠁⠀⢠⣤⣤⣶⣤⣤⣤⡀⠈⠑⠠⢄⠈⠁⠀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠋⠀⢴⠋⠀⠀⠰⣧⠀⢸⣿⣿⣿⣿⣿⣿⡇⠀⣴⣄⠀⠑⠢⣤⡀⠙⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠁⢀⣄⠀⠀⢾⣦⠀⠙⠦⠀⠙⠿⠿⠿⠿⠋⠀⣴⠋⠁⣀⣤⣠⣿⣷⡀⠈⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠁⢀⠀⠙⢷⣶⣾⣿⣷⣤⣄⣰⣦⣄⣀⣀⣠⣴⣾⣿⣷⠾⠿⠀⠈⠉⠛⠓⠀⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⡟⠀⢀⠈⠓⢤⣀⠉⠙⠻⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣅⣀⣠⣤⣄⡀⠀⠒⠲⠶⠄⠀⢻⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠉⠀⠀⠀⠙⠷⣶⣤⣤⣀⣀⣀⡉⠉⣹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣦⣤⣀⣀⣀⠀⠹⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⠏⠀⣰⣿⣷⣄⡀⠙⠢⡀⠈⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆⠀⠹⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣇⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣀⣸⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
# ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
from filter_profanity import ban_filter
from generate_text import generate_text
from say import say, play_sounds


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
    _message = ban_filter(_message, config.ban_words)
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               "]+", flags=re.UNICODE)
    _message = emoji_pattern.sub(r'', _message)
    if "[ERROR]" not in _message:
        connection = twitch_chat_irc.TwitchChatIRC(config.bot_name, api_keys.twitch)
        _message.replace("\n", "")
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
    r = sr.Recognizer()
    while True:
        message = ""
        with sr.Microphone() as source:
            if not config.DEBUG_MODE:
                os.system('cls')
            print(
                "[audio_ai]: " + bcolors.FAIL + "=============================== Я СЛУШАЮ ВАС =================================" + bcolors.ENDC)
            r.adjust_for_ambient_noise(source)
            audio_text = r.listen(source, phrase_time_limit=15)
            if not config.DEBUG_MODE:
                os.system('cls')
            print(
                "[audio_ai]: " + bcolors.OKBLUE + "=============================== РАСПОЗНАЮ ЗВУК ===============================" + bcolors.ENDC)

        try:
            recognisingResult = r.recognize_google(audio_text, language="ru-RU", show_all=True)
            if not str(recognisingResult) == "[]":
                if not config.DEBUG_MODE:
                    print("\n\n")
                    for transcript in recognisingResult['alternative']:
                        print(transcript['transcript'])
                    print("\n\n")
                transcript = recognisingResult['alternative'][0]['transcript']
                confidence = recognisingResult['alternative'][0]['confidence']
                print("[audio_ai]: " + str(confidence))
                print("[audio_ai]: " + bcolors.OKCYAN + transcript + bcolors.ENDC)
                # if config.CALL_BY_NAME_MODE and config.CALL_NAME in transcript.lower():
                message = generate_text(transcript.replace(config.CALL_NAME, ""))
                # else:
                #    print("[audio_ai]: Обращения не найдено")
            else:
                print(
                    "[audio_ai]: " + bcolors.WARNING + "=============================== НЕ СЛЫШУ НИХУЯ ===============================" + bcolors.ENDC)
        except Exception as e:
            print(e)

        if message != "":
            # print("[audio_ai][second_response]: " + bcolors.OKGREEN + message + bcolors.ENDC)
            if not config.stream_mode:
                send_message(prettify(message))
            #say(message)
            sleep_time = random.randint(20, 45)
            print("[audio_ai]: " + "Sleeping for: " + str(sleep_time))
            if not config.FAST_SLEEP:
                time.sleep(sleep_time)


def handle_message(message):
    decoded_tag = message['display-name']
    decoded_message = message['message']
    if "@" + config.bot_name.lower() in str(decoded_message).lower():
        print("[text_ai]: " + bcolors.OKGREEN + str(decoded_message) + bcolors.ENDC)

        ai_message = generate_text(decoded_message)
        pattern = re.compile(re.escape("@" + config.bot_name.lower()), re.IGNORECASE)
        ai_message = pattern.sub("", ai_message)
        decoded_message = pattern.sub("", decoded_message)
        if "@" + config.bot_name.lower() in decoded_tag:
            print("Пытались наебать")
        else:
            ai_message = "@" + decoded_tag + " " + ai_message

        # print("[text_ai][second_response]: " + bcolors.OKGREEN + ai_message + bcolors.ENDC)
        ai_message.replace("\n", " ")
        if config.stream_mode:
            print(f"IM SAYING: {decoded_message} {ai_message}")
            ai_message = ai_message.replace("@", "")
            say(decoded_message + " . " + ai_message)
        else:
            ai_message = add_emojis(ai_message)
            send_message(ai_message)
    else:
        print("[text_ai]: " + bcolors.WARNING + str(decoded_message) + bcolors.ENDC)


def text_ai():
    connection = twitch_chat_irc.TwitchChatIRC(config.bot_name, api_keys.twitch)
    connection.listen(config.streamer, on_message=handle_message)
    connection.close_connection()


def init_ban_filter():
    temp_ban_list = []
    with open('nigga', encoding='utf8') as f:
        temp_ban_list = f.readlines()
    for word in temp_ban_list:
        config.ban_words.append(word.replace("\n", ""))


if __name__ == "__main__":
    init_ban_filter()

    print(config.ban_words)
    print(
        bcolors.OKGREEN + f"\n\nStarting with params:\n streamer: {config.streamer}\n stream_mode = {config.stream_mode}\n FAST_SLEEP = {config.FAST_SLEEP}\n DISABLE_TEXT = {config.DISABLE_TEXT}\n DISABLE_AUDIO = {config.DISABLE_AUDIO}\n DEBUG_MODE = {config.DEBUG_MODE}\n\n" + bcolors.ENDC)
    sound_thread = threading.Thread(target=play_sounds, daemon=True)
    sound_thread.start()
    # if not config.DISABLE_TEXT:
    text_ai_thread = threading.Thread(target=text_ai, args=())
    text_ai_thread.start()
    # if not config.stream_mode and not config.DISABLE_AUDIO:
    audio_ai_thread = threading.Thread(target=audio_ai, args=())
    audio_ai_thread.start()