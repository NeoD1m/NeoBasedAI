import openai
import config
import api_keys
import threading
import re
import requests
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
from twitch_chat_irc import twitch_chat_irc
import random

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


def say(_message):
    url = 'https://tts.voicetech.yandex.net/tts?&format=mp3&lang=ru_RU&speed=1.3&emotion=good&speaker=ermil_with_tuning&robot=1&text=' + _message
    response = requests.get(url)
    audio = AudioSegment.from_file(BytesIO(response.content), format="mp3")
    play(audio)


def insert_word(original_string, new_word):
    # Find all word boundaries in the original string
    word_boundaries = [match.start() for match in re.finditer(r'\b', original_string)]

    # Choose a random word boundary to insert the new word after
    random_boundary = random.choice(word_boundaries)

    # Insert the new word after the chosen boundary
    new_string = original_string[:random_boundary] + new_word + original_string[random_boundary:]

    return new_string

def handle_message(message):
    decoded_tag = message['display-name']
    decoded_message = message['message']
    if "@neobased" in str(decoded_message).lower() or "@neobasedai" in str(decoded_message).lower():
        print("[text_ai]: " + bcolors.OKGREEN + str(decoded_message) + bcolors.ENDC)
        response = openai.Completion.create(
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

        ai_message = insert_word(ai_message, " бля ")

        pattern = re.compile(re.escape("@neobased"), re.IGNORECASE)
        ai_message = pattern.sub("", ai_message)

        decoded_message = pattern.sub("", decoded_message)
        ai_message = decoded_message + ", " + decoded_tag + ", " + ai_message

        print("[text_ai][second_response]: " + bcolors.OKGREEN + ai_message + bcolors.ENDC)
        say(ai_message)
    else:
        print("[text_ai]: " + bcolors.WARNING + str(decoded_message) + bcolors.ENDC)


def text_ai():
    connection = twitch_chat_irc.TwitchChatIRC('NeoBased', api_keys.twitch)
    connection.listen(config.streamer, on_message=handle_message)
    connection.close_connection()


if __name__ == "__main__":
    openai.api_key = api_keys.openai
    text_ai_thread = threading.Thread(target=text_ai, args=())
    text_ai_thread.start()
