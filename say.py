import os
import random
import time

from playsound import playsound

import config
import requests

from filter_profanity import ban_filter


def say(_message):
    if config.DEBUG_MODE:
        print("SAY")
    config.message_queue.put(_message)


def play_sounds():
    while True:
        _message = config.message_queue.get()
        _message = ban_filter(_message, config.ban_words)
        #print(f"LOCK: {config.audio_lock}")
        with config.audio_lock:
            if config.USE_YARICK_VOICE:
                base_voice = 'https://tts.voicetech.yandex.net/tts?&format=mp3&lang=ru_RU&speed=1.0&emotion=neutral&speaker=oksana&robot=1&text='
            else:
                base_voice = 'https://tts.voicetech.yandex.net/tts?&format=mp3&lang=ru_RU&speed=1.0&emotion=good&speaker=erkanyavas&robot=1&text='

            url = base_voice + _message
            response = requests.get(url)

            try:
                if response.status_code == 200 and response:
                    random_num = random.randrange(200)
                    with open(f'file{random_num}.mp3', 'wb') as f:
                        f.write(response.content)

                    playsound(f'./file{random_num}.mp3', block=True)

                    os.remove(f'file{random_num}.mp3')
                    if not config.message_queue.empty():
                        if config.stream_mode:
                            time.sleep(4)
                        else:
                            time.sleep(1)
                else:
                    #print('[AUDIO] Error', response.status_code)
                    if response.status_code == 504:
                        if config.DEBUG_MODE:
                            print("[ERROR GETTING AUDIO] retrying...")
                        config.message_queue.put_nowait(_message)
                        #say(_message)
            finally:
                if config.DEBUG_MODE:
                    print("[AUDIO COMPLETED]")

def say2(_message):
    with config.audio_lock:
        if config.USE_YARICK_VOICE:
            base_voice = 'https://tts.voicetech.yandex.net/tts?&format=mp3&lang=ru_RU&speed=1.0&emotion=neutral&speaker=nick&robot=1&text='
        else:
            base_voice = 'https://tts.voicetech.yandex.net/tts?&format=mp3&lang=ru_RU&speed=1.0&emotion=good&speaker=erkanyavas&robot=1&text='

        url = base_voice + _message
        response = requests.get(url)

        try:
            if response.status_code == 200 and response:
                random_num = random.randrange(200)
                with open(f'file{random_num}.mp3', 'wb') as f:
                    f.write(response.content)

                playsound(f'./file{random_num}.mp3', block=True)

                os.remove(f'file{random_num}.mp3')
            else:
                print('[AUDIO] Error', response.status_code)
                if response.status_code == 504:
                    config.audio_lock.release()
                    say(_message)
        finally:
            print("[AUDIO BRUH]")
# def say(_message):
#    url = 'https://tts.voicetech.yandex.net/tts?&format=mp3&lang=ru_RU&speed=1.3&emotion=good&speaker=ermil_with_tuning&robot=1&text=' + _message
#    response = requests.get(url)
#    audio = AudioSegment.from_file(BytesIO(response.content), format="mp3")
#    play(audio)
#
# if __name__ == "__main__":
#    say("Добрый вечер бля чат, сегодня мой первый стрим. Устроим аукцион на фильм, сериал или аниме. Будем смотреть до конца, никаких ограничений нет")
