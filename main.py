from playsound import playsound
import speech_recognition as sr
from speech_recognition import UnknownValueError
from googletrans import Translator
from gtts import gTTS
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import asyncio
import wave


SAMPLING_RATE = 48000
CHANNELS = 2
FRAME_WIDTH = 2


########################################
# SETUP VARIABLES
########################################

lang = 'de'
speak_length = 10
filename = 'test1.wav'
# output_path for MP3Sink will be available in version 2.1

########################################
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
    await asyncio.sleep(speak_length)
    print("Finished recording.\n")
    connected.stop_recording()


async def transcribe_audio(sink, channel):
    user_ids = [user_id for user_id, audio in sink.audio_data.items()]
    # recorded_users = [f"{user_id}" for user_id, audio in sink.audio_data.items()]
    await sink.vc.disconnect()
    files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]
    # await text_channel.send("Here's a recording!", files=files)

    f = wave.open(filename, 'w')
    f.setframerate(SAMPLING_RATE)
    f.setnchannels(CHANNELS)
    f.setsampwidth(FRAME_WIDTH)
    f.writeframes(files[0].fp.read())
    f.writeframes(b'')

    r = sr.Recognizer()
    sinkfile = sr.AudioFile(filename)

    with sinkfile as source:
        print("listening...")
        audio = r.record(source)  # use record to get from file
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-US', show_all=True)
            transcript = query['alternative'][0]['transcript']
            print(f"User said: {transcript}\n")
        except UnknownValueError as e:
            print("Did not copy.")
            print(str(e))
            return "None"

    translator = Translator()

    text_to_translate = translator.translate(transcript, dest=lang)
    text = text_to_translate.text

    print(text)

    speak = gTTS(text=text, lang=lang, slow=False)
    speak.save("translate.mp3")
    playsound('translate.mp3')
    os.remove('translate.mp3')

    # return query

# query = transcribe_audio()
# while (query == "None"):
#     query = transcribe_audio()



bot.run(TOKEN)