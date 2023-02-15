import speech_recognition as sr
import openai
import time
import config
import api_keys
import translator
import random
import asyncio
import concurrent.futures
import threading

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
            print("Listening")
            audio_text = r.listen(source, phrase_time_limit=10)
            print("Recognising")

        try:
            recognisingResult = r.recognize_google(audio_text, language="ru-RU", show_all=True)
            transcript = recognisingResult['alternative'][0]['transcript']
            confidence = recognisingResult['alternative'][0]['confidence']
            print(str(confidence))
            print(bcolors.OKCYAN + transcript + bcolors.ENDC)
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
                print(bcolors.WARNING + message + bcolors.ENDC)
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
                print("Small input")
        except Exception as e:
            print(e)

        if message != "":
            print(bcolors.OKGREEN + message + bcolors.ENDC)

            send_message(prettify(message))
            randomAdditionalSeconds = random.randint(0, 30)
            print("Sleeping for: " + str(randomAdditionalSeconds))
            if not FAST_SLEEP:
                time.sleep(2)


def text_ai():
    while True:
        print(bcolors.FAIL + "todo text" + bcolors.ENDC)
        time.sleep(2)


if __name__ == "__main__":
    text_ai_thread = threading.Thread(target=text_ai, args=())
    text_ai_thread.start()
    audio_ai_thread = threading.Thread(target=audio_ai, args=())
    audio_ai_thread.start()
