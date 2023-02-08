import speech_recognition as sr
import openai
import time
import config
import api_keys
import translator

from twitch_chat_irc import twitch_chat_irc



def send_message(message):
    connection = twitch_chat_irc.TwitchChatIRC('NeoBased', api_keys.twitch)
    connection.send(config.streamer, message)
    connection.close_connection()


openai.api_key = api_keys.openai
r = sr.Recognizer()

while (True):
    message = ""
    with sr.Microphone() as source:
        print("Listening")
        audio_text = r.listen(source, phrase_time_limit=10)
        print("Recognising")

    try:
        transcript = r.recognize_google(audio_text, language="ru-RU", show_all=True)['alternative'][0]['transcript']
        if len(transcript.split(" ")) >= 4:
            print(transcript)

            #if config.use_translator:
            #    to_en = translator.to_en(transcript)
            #    print (to_en)
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt="напиши неформальный смешной комментарий на данное сообщение: \"" + transcript + "\". в случайное место вставь слово бля",
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                best_of=1,
                frequency_penalty=2,
                presence_penalty=0
            )
            message = response["choices"][0]["text"].replace("\"", "").replace("\n","")
            #print(message)
            #message = translator.to_ru(message)
        else:
            print("Small input")
    except Exception as e: print(e)

    if message != "":
        print('\033[93m' + message + '\033[0m')
        send_message("@" + config.streamer + " " + message)
        time.sleep(45)