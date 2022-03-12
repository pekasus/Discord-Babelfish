from playsound import playsound
import sounddevice as sd
import speech_recognition as sr
from speech_recognition import UnknownValueError
from googletrans import Translator
from gtts import gTTS
import os



def translate_from_file():
    filename = 'test.wav'

    # playsound(filename)
    sinkfile = sr.AudioFile(filename)
    # sinkfile = sr.AudioFile('test.wav')
    r = sr.Recognizer()
    # with sr.Microphone() as source:
    with sinkfile as source:
        print("listening...")
        # r.pause_threshold = 15
        # audio = r.listen(source)  # this listens to microphone
        audio = r.record(source)  # use record to get from file
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, key=None, language='en-US', show_all=True)
            print(f"User said: {query}\n")
        except UnknownValueError as e:
            print("Did not copy.")
            print("Exception: " + str(e))

    # query = "This is a test of the national broadcasting service."

    translator = Translator()
    lang = 'pt'

    input_text = query['alternative'][0]['transcript']
    text_to_translate = translator.translate(input_text, dest=lang)
    text = text_to_translate.text

    print(text)

    speak = gTTS(text=text, lang=lang, slow=False)
    speak.save("translate.mp3")
    playsound('translate.mp3')
    os.remove('translate.mp3')


def translate_from_mic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 2
        audio = r.listen(source)  # this listens to microphone (I think)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, key=None, language='en-US', show_all=True)
            print(f"User said: {query}\n")
        except UnknownValueError as e:
            print("Did not copy.")
            print("Exception: " + str(e))

    translator = Translator()
    lang = 'ru'

    input_text = query['alternative'][0]['transcript']
    text_to_translate = translator.translate(input_text, dest=lang)
    text = text_to_translate.text


    speak = gTTS(text=text, lang=lang, slow=False)
    speak.save("translate.mp3")
    playsound('translate.mp3')
    os.remove('translate.mp3')

# translate_from_mic()
translate_from_file()