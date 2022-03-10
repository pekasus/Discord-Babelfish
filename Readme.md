# Discord Babelfish
This bot will listen to live stage events and create translation channels 
to translate the audio into any language and broadcast it simultaneously in 
the different channels.

## Process Overview
The target is to get the bot to handle streaming audio and translate it in 
near real time, but for development purposes, it will start out recording 
a 15 second segment and translate it as a chunk. Once this is worked out, the 
process will be changed to break up chunks by pause and translate them closer 
to real time.

### Steps
1. Record a 15 second clip of audio.
2. Transcribe the audio into text.
3. Translate the text into the target language.
4. Use text to voice to create a clip of audio in the target langauge.
5. Play the translated audio file and broadcast to another channel.
6. Delete the translated audio file.

### Libraries
1. Pycord
2. SpeechRecognition
3. googletrans
4. PyAudio
5. gTTS
6. asyncio

### Issues
I'm having trouble installing PyAudio in a virtual environment because it 
requires `sudo` to install and this creates issues with maintaining the 
environment and accessing the files. For now, I'm not using a virtual 
environment

install pyaudio: https://stackoverflow.com/questions/55984129/attributeerror-could-not-find-pyaudio-check-installation-cant-use-speech-re

Another issue is that I can't install Pycord 2.1 yet. The latest install 
version through the GitHub repository seems to be 2.0.0b5. Some of the 
audio features seem to require version 2.1, so it is possible that this 
won't work until version 2.1 is released.