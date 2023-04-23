import threading
from queue import Queue

bot_name = "NeoBased"

stream_mode = True
DIALOG_MODE = False
FAST_SLEEP = True

DISABLE_TEXT = False
DISABLE_AUDIO = False

USE_YARICK_VOICE = False

audio_lock = threading.Lock()
message_queue = Queue()

DEBUG_MODE = True

CALL_BY_NAME_MODE = False # не работает забей хуй
CALL_NAME = "база"
if stream_mode:
    streamer = bot_name
else:
    streamer = "dawgdebik"

prompt_base = "Тебя зовут NeoBased.Ты стример на твиче и это твой дебютный стрим, отвечай смешно и немного тролль, но будь добрым.В свой ответ вставляй слово бля.Не используй смайлики или эмодзи в ответе.Ответь на сообщение, не упоминай текст выше:\n"
#Сегодня ты общаешься со стримером МайтиПут, отвечай ему.
#Коротко ответь на следующее сообщение
#Твой и создатель отец: NeoDimLIVE, упоминай его только когда тебя о нём спросят.
#Говори ТОЛЬКО по древнерусски, как настоящий славянин.
#,твоя мама: @DawgDebik, твой парень: @jidinkii, твоя младшая сестричка: @SlavMayer, упоминай их только если тебя напрямую спросят о семье.
if streamer == "MightyPoot":
    emojis = ["LUL", "NotLikeThis", "BibleThump", "pootDog", "pootLove", "pootComf", "pootStare", "pootDogWhat"]
else:
    emojis = ["LUL", "NotLikeThis", "BibleThump"]

# emojis = ["pootHehe","BibleThump","pootDogWhat","pootBodiesHitTheFloor","pootStare","LUL","NotLikeThis","pootLove","pootDog","pootYepcoke","pootChatBeLIke"]

ban_words = []


# DISABLE_TEXT = True
# stream_mode = True
# input Line 1
# output default