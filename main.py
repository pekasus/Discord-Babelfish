from playsound import playsound
import sounddevice as sd
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 2
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

# query = "translate this text into russian"

translator = Translator()

text_to_translate = translator.translate(query, dest='ru')
text = text_to_translate.text

print(text)

speak = gTTS(text=text, lang='ru', slow=False)
speak.save("test.mp3")
playsound('test.mp3')
os.remove('test.mp3')

