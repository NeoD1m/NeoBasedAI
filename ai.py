import speech_recognition as sr
import openai
import time

from twitch_chat_irc import twitch_chat_irc

streamer = "plaintsoup"

def send_message(message):
    connection = twitch_chat_irc.TwitchChatIRC('NeoBased', 'oauth:5msd8npngbtp1hewmyh2sw37ejawm1')
    connection.send("plaintsoup", message)
    connection.close_connection()


openai.api_key = "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"
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
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt="напиши смешной комментарий на это сообщение: \"" + transcript + "\"",
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                best_of=3,
                frequency_penalty=0,
                presence_penalty=0
            )
            print(response)
            message = response["choices"][0]["text"].replace("\"", "").replace("\n","")
        else:
            print("Small input")
    except Exception as e: print(e)

    if message != "":
        print(message)
        send_message("@" + "plaintsoup" + " " + message)
        time.sleep(45)