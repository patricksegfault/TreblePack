# TreblePack

## Dependencies
Install Python 3.8+
https://www.python.org/ftp/python/3.8.0/python-3.8.0.exe

Requires requests, pydub and simpleaudio python packages. 

Open the command prompt and run the following commands:
- pip3 install requests
- pip3 install pydub
- pip3 install simpleaudio

On Windows 10 - 

Download the build for ffmpeg (4.2.1+)

https://ffmpeg.zeranoe.com/builds/

Extract and add the /bin directory to your PATH

## How to setup and run
You will need to first add music into the music folder.

This version only plays mp3 files (more formats to be added later)

In the TT.json file you will need to define your own triggers for what cards in play, play what music

Here are the fields you will need to populate:

localPlayer - true (enemy cards for triggers currently not supported)

card - Name of card as found in the set1-en_us-small.json file

playMusic - name_of_your_music.mp3

If you change your default port, you will need to update the port field in TT.json

Run treble.py at the command prompt (or in IDLE)

## Future
- More music format support
- Triggers for enemy cards
- Triggers for draw/in-hand cards
- Triggers for in-play cards
- Allow for triggers to play playlists
- UI for ease of use creating triggers
- Triggers for expeditions
- Triggers for specific decks
