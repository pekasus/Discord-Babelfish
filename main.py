from playsound import playsound
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Did not copy.")
        return "None"

    return query

query = takecommand()
while (query == "None"):
    query = takecommand()



