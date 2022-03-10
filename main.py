from playsound import playsound
import sounddevice as sd
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
GUILD = int(os.getenv('GUILD_ID'))
AUDIO_CHANNEL = int(os.getenv('AUDIO_CHANNEL'))


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
    global guild, channel
    guild = bot.get_guild(GUILD)
    channel = bot.get_channel(AUDIO_CHANNEL)
    connected = await channel.connect()
    connected.start_recording(discord.sinks.MP3Sink(output_path='test.mp3'), transcribe_audio)
    print("Recording...\n")
    await asyncio.sleep(15)
    print("Finished recording.\n")
    connected.stop_recording()


async def transcribe_audio():
    filename = 'test.mp3'
    r = sr.Recognizer()
    sinkfile = sr.AudioFile(filename)
    # with sr.Microphone() as source:
    with sinkfile as source:
        print("listening...")
        # r.pause_threshold = 15
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en')
        print(f"User said: {query}\n")
    except Exception as e:
        print("Did not copy.")
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

# query = "translate this text into another language"




bot.run(TOKEN)