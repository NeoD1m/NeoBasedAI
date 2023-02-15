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

from twitch_chat_irc import twitch_chat_irc

# emojis = ["pootHehe","BibleThump","pootDogWhat","pootBodiesHitTheFloor","pootStare","LUL","NotLikeThis","pootLove","pootDog","pootYepcoke","pootChatBeLIke"]
emojis = ["LUL", "NotLikeThis", "BibleThump", "pootDog", "pootLove", "pootComf", "pootStare", "pootDogWhat"]
# emojis = ["LUL", "NotLikeThis", "BibleThump"]
FAST_SLEEP = False


# https://pypi.org/project/twitch-chat-irc/
# https://platform.openai.com/account/api-keys

# TODO
# https://github.com/lacson/webcaptioner-stream распознование звука

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
    connection = twitch_chat_irc.TwitchChatIRC('NeoBased', api_keys.twitch)
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
        emojiNumber = random.randint(0, len(emojis) - 1)
        amount = random.randint(1, 3)
        return _message + " " + ((emojis[emojiNumber] + " ") * amount)
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
            if len(transcript.split(" ")) >= 4:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt="give a new short and funny answer to this message: \"" + transcript + "\"",
                    temperature=0.75,
                    max_tokens=256,
                    top_p=1,
                    best_of=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                message = response["choices"][0]["text"].replace("\"", "").replace("\n", "")
                message = message.replace("!", "")
                print("[audio_ai][first_response]: " + bcolors.WARNING + message + bcolors.ENDC)
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt="вставь слово бля в случайное место в этом сообщении: \"" + message + "\"",
                    temperature=0.7,
                    max_tokens=256,
                    top_p=1,
                    best_of=1,
                    frequency_penalty=0,
                    presence_penalty=0
                )
                message = response["choices"][0]["text"].replace("\"", "").replace("\n", "")
                message = message.replace("!", "")
            else:
                print("[audio_ai]: " + "Small input")
        except Exception as e:
            print(e)

        if message != "":
            print("[audio_ai][second_response]: " + bcolors.OKGREEN + message + bcolors.ENDC)

            send_message(prettify(message))
            sleep_time = random.randint(5, 30)
            print("[audio_ai]: " + "Sleeping for: " + str(sleep_time))
            if not FAST_SLEEP:
                time.sleep(sleep_time)


def handle_message(message):
    decoded_tag = message['display-name']
    decoded_message = message['message']
    if "@neobased" in str(decoded_message).lower():
        print("[text_ai]: " + bcolors.OKGREEN + str(decoded_message) + bcolors.ENDC)
        response = openai.Completion.create( #TODO рефактор генерации
            model="text-davinci-003",
            prompt="give a new short and funny answer to this message: \"" + decoded_message + "\"",
            temperature=0.75,
            max_tokens=256,
            top_p=1,
            best_of=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        ai_message = response["choices"][0]["text"].replace("\"", "").replace("\n", "")
        ai_message = ai_message.replace("!", "")
        print("[text_ai][first_response]: " + bcolors.WARNING + ai_message + bcolors.ENDC)
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt="вставь слово бля в случайное место в этом сообщении: \"" + ai_message + "\"",
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            best_of=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        ai_message = response["choices"][0]["text"].replace("\"", "").replace("\n", "").replace("!", "")
        pattern = re.compile(re.escape("@neobased"), re.IGNORECASE)
        ai_message = pattern.sub("", ai_message)
        ai_message = "@" + decoded_tag + " " + ai_message
        ai_message = add_emojis(ai_message)
        print("[text_ai][second_response]: " + bcolors.OKGREEN + ai_message + bcolors.ENDC)
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
    audio_ai_thread = threading.Thread(target=audio_ai, args=())
    audio_ai_thread.start()
