import requests
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play

URL = "https://tts.voicetech.yandex.net/tts"


def say(_message):
    params = {
        "format": "mp3",
        "lang": "ru_RU",
        "speed": 1.3,
        "emotion": "good",
        "speaker": "ermil_with_tuning",
        "robot": 1,
        "text": _message,
    }
    response = requests.get(URL, params=params)
    audio = AudioSegment.from_file(BytesIO(response.content), format="mp3")
    play(audio)


if __name__ == "__main__":
    say(
        "Добрый вечер бля чат, сегодня мой первый стрим. Устроим аукцион на фильм, сериал или аниме. Будем смотреть до конца, никаких ограничений нет"
    )
