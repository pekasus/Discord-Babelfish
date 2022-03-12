from playsound import playsound
import sounddevice as sd
import speech_recognition as sr
from speech_recognition import UnknownValueError
from googletrans import Translator
from gtts import gTTS
import os




filename = 'test.wav'

# playsound(filename)

sinkfile = sr.AudioFile(filename)
print(dir(sinkfile))
r = sr.Recognizer()
# with sr.Microphone() as source:
with sinkfile as source:
    print("listening...")
    # r.pause_threshold = 15
    # audio = r.listen(source)  # this listens to microphone (I think)
    audio = r.record(source)  # use record to get from file
    print(type(audio))
try:
    print("Recognizing...")
    query = r.recognize_google(audio, language='en-US', show_all=True)
    print(f"User said: {query}\n")
except UnknownValueError as e:
    print("Did not copy.")
    print(str(e))

query = "This is a test of the national broadcasting service."

translator = Translator()
lang = 'pt'

text_to_translate = translator.translate(query, dest=lang)
text = text_to_translate.text

print(text)

speak = gTTS(text=text, lang=lang, slow=False)
speak.save("translate.mp3")
playsound('translate.mp3')
os.remove('translate.mp3')
