from time import sleep
from requests import get as getReq
from pydub import AudioSegment
from pydub.playback import play
import tkinter as tk
from threading import Thread
import json
import sys
import os

global debug
debug = False

def playMusic(triggerPassed, settings, stopMusic):
    second = 1000
    song = AudioSegment.from_mp3(os.getcwd()+"\\music\\"+triggerPassed['playMusic'])
    songLengthSec = len(song) // second
    for sec in range(0, songLengthSec//5):
        startSplit = sec*second*5
        endSplit = (sec+1)*second*5
        if stopMusic():
            play(song[startSplit:endSplit].fade_out(second))
            break
        if sec == 0:
            play(song[startSplit:endSplit].fade_in(second))
        else:
            play(song[startSplit:endSplit])
    return

def checkTriggers(triggers, data, cardTransDict):
    triggerPassed = {}
    cards = data['Rectangles']
    
    for card in cards:
        if card['CardCode'] != "face":
            for i, trigger in enumerate(triggers):
                if (trigger['localPlayer'] == card['LocalPlayer'] and
                    abs(card['TopLeftY']-260) <= 5 and (card['Height']-160) <= 5 and #on bench
                    trigger['card'] == cardTransDict[card['CardCode']]):
                        triggerPassed = trigger
                        triggerPassed['triggerNum'] = i
                        break
        if len(triggerPassed) > 0:
            break
            
    return triggerPassed

def printTriggers(settings):
    for trigger in settings['triggers']:
        print("Trigger for the local player? " + str(trigger['localPlayer']))
        print("Under what action should this happen? " + trigger['action'])
        print("What card is the trigger? " + trigger['card'])
        if trigger['isPlaylist']:
            print("Play this playlist: " + str(settings['playlists'][trigger['playMusic']]))
        else:
            print("Play this music: " + trigger['playMusic'])
        print("")
    return

def loadSettings():
    with open("TT.json", "r") as file:
        data = json.load(file)
    return data

def saveSettings(settings):
    with open("TT.json", "w") as file:
        json.dump(settings, file)
    return

def genCardTransDict():
    cardTransDict = {}

    with open("set1-en_us-small.json", 'r', encoding='utf-8') as file:
        cardTransDict = json.load(file)
    
    return cardTransDict

def printGame(data, cardTransDict):
    global debug
    cards = data['Rectangles']
    
    for card in cards:
        if card['CardCode'] != "face":
            if card['LocalPlayer']:
                # values keep moving a little but they should be within 5 of these values
                if abs(card['TopLeftY']-450) <= 5 and abs(card['Height']-155) <= 5: #inplay
                    print("Card IN PLAY: " + cardTransDict[card['CardCode']])
                elif abs(card['TopLeftY']-260) <= 5 and (card['Height']-160) <= 5: #bench
                    print("Card ON BENCH: " + cardTransDict[card['CardCode']])
                elif abs(card['TopLeftY']-720) <= 5 and abs(card['Height']-370) <= 5: #draft
                    print("Card DRAFT: " + cardTransDict[card['CardCode']])
                else:
                    print("Card IN HAND: " + cardTransDict[card['CardCode']])
            else:
                print("><>< Enemy Card: " + cardTransDict[card['CardCode']])
            if debug:
                print("X, Y, H/W: "+str(card['TopLeftX'])+", "+str(card['TopLeftY'])+", "+str(card['Height'])+"/"+str(card['Width']))
            print("")
    print(" --- --- --- --- --- ")
    return

def activeDeck(port):
    global debug
    req = getReq("http://localhost:"+port+"/static-decklist")
    if debug:
        print(req.text)
    req = req.json()
    return req

def cardPositions(port):
    global debug
    req = getReq("http://localhost:"+port+"/positional-rectangles")
    if debug:
        print(req.text)
    req = req.json()
    return req

req = False
defaultSleep = 2
cardTransDict = genCardTransDict()
settings = loadSettings()
port = settings['port']
stopMusic = False
triggerPassed = {}
musicThread = Thread(target = playMusic, args = (triggerPassed, settings, lambda: stopMusic))

try:
    req = activeDeck(port)
except Exception:
    while (not req):
        print("Waiting for Runeterra to open...")
        sleep(defaultSleep)
        try:
            req = activeDeck(port)
        except Exception:
            continue

while(True):
    sleep(defaultSleep)
    gameReq = cardPositions(port)
    while(gameReq['GameState'] == 'InProgress'):
        triggerPassed = checkTriggers(settings['triggers'], gameReq, cardTransDict)
        if len(triggerPassed) > 0:
            settings['triggers'][triggerPassed['triggerNum']]['card'] = '' #trigger won't happen again
            if musicThread.is_alive():
                stopMusic = True
                musicThread.join()
                stopMusic = False
            musicThread = Thread(target = playMusic, args = (triggerPassed, settings, lambda: stopMusic))
            musicThread.start()
        if debug:
            printGame(gameReq, cardTransDict)
        sleep(defaultSleep*3)
        gameReq = cardPositions(port)
    settings = loadSettings()
