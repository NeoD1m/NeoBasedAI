import speech_recognition as sr
import openai
import time
import config
import api_keys
import translator
import random

from twitch_chat_irc import twitch_chat_irc

# emojis = ["pootHehe","BibleThump","pootDogWhat","pootBodiesHitTheFloor","pootStare","LUL","NotLikeThis","pootLove","pootDog","pootYepcoke","pootChatBeLIke"]
emojis = ["LUL", "NotLikeThis", "BibleThump"]

FAST_SLEEP = True


def send_message(_message):
    connection = twitch_chat_irc.TwitchChatIRC('NeoBased', api_keys.twitch)
    connection.send(config.streamer, _message)
    connection.close_connection()


uList = ["ты", "тебя", "тебе", "твои", "твой", "тобой"]


def add_tag(_message):
    randomNumber = random.randint(0, 7)
    if uList in _message:
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
        print("\033[96mconfidence: " + str(confidence) + '\033[0m')
        print("\033[96m" + transcript + '\033[0m')
        if len(transcript.split(" ")) >= 4:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt="напиши смешной короткий комментарий на данное сообщение: \"" + transcript + "\", обращайся на ты",
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                best_of=3,
                frequency_penalty=0,
                presence_penalty=0
            )
            message = response["choices"][0]["text"].replace("\"", "").replace("\n", "")
            message = message.replace("!", "")
            print('\033[93m' + message + '\033[0m')
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
            print("Small input or not recognised")
    except Exception as e:
        print(e)

    if message != "":
        print('\033[92m' + message + '\033[0m')

        send_message(prettify(message))
        randomAdditionalSeconds = random.randint(5, 35)
        print("Sleeping for: " + str(randomAdditionalSeconds + 30))
        if not FAST_SLEEP:
            time.sleep(30 + randomAdditionalSeconds)
