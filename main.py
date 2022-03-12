import io

from playsound import playsound
import sounddevice as sd
import speech_recognition as sr
from speech_recognition import UnknownValueError
from googletrans import Translator
from gtts import gTTS
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio

########################################

# output_path for MP3Sink will be available in version 2.1

########################################

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
GUILD = int(os.getenv('GUILD_ID'))
AUDIO_CHANNEL = int(os.getenv('AUDIO_CHANNEL'))
TEXT_CHANNEL = int(os.getenv('TEXT_CHANNEL'))


intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.reactions = True
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

async def listen():
    pass


@bot.event
async def on_ready():
    global guild, channel, text_channel
    guild = bot.get_guild(GUILD)
    channel = bot.get_channel(AUDIO_CHANNEL)
    text_channel = bot.get_channel(TEXT_CHANNEL)

    connected = await channel.connect()
    # Need to use .wav file for speech_recognition
    connected.start_recording(discord.sinks.WaveSink(), transcribe_audio, channel)
    print("Recording...\n")
    await asyncio.sleep(5)
    print("Finished recording.\n")
    connected.stop_recording()


async def transcribe_audio(sink, channel):
    # user_ids = [user_id for user_id, audio in sink.audio_data.items()]
    # recorded_users = [f"{user_id}" for user_id, audio in sink.audio_data.items()]
    await sink.vc.disconnect()
    files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]
    # await text_channel.send("Here's a recording!", files=files)

    filename = 'test.wav'
    b = io.BytesIO(files[0].fp.read())
    with open(filename, 'wb') as f:
        f.write(b.read())

    playsound(filename)

    r = sr.Recognizer()
    sinkfile = sr.AudioFile(filename)
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
        return "None"

    translator = Translator()

    text_to_translate = translator.translate(query, dest='de')
    text = text_to_translate.text

    print(text)

    speak = gTTS(text=text, lang='de', slow=False)
    speak.save("translate.mp3")
    playsound('translate.mp3')
    os.remove('translate.mp3')

    # return query

# query = transcribe_audio()
# while (query == "None"):
#     query = transcribe_audio()




bot.run(TOKEN)