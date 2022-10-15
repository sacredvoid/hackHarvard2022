import json
import os
from pydub import AudioSegment
from data import SOUND_PATH, JSON_DICT_PATH, TEMP_FILES_PATH, INTENSITY_MAP_PATH

def increaseDuration(sound, factor):
    for i in range(0, factor):
        sound = sound.append(sound, crossfade=400)
    return sound


def textToSound(textArray):
    filePath = SOUND_PATH

    # Open JSON file to dictionary. # fetch from API ///////////////////////////////////////////////////////////
    jsonFileName = JSON_DICT_PATH
    with open(jsonFileName) as json_file:
        jsonDict = json.load(json_file)

    # Set loudness based on intensity map
    # fetch from API ///////////////////////////////////////////////////////////
    jsonFileName = INTENSITY_MAP_PATH
    with open(jsonFileName) as json_file:
        intensityMap = json.load(json_file)

    sound1 = AudioSegment.from_file(filePath + jsonDict[textArray[0]][0])  # First sound from textArray
    for t in textArray[1:]:
        sound2 = AudioSegment.from_file(filePath + jsonDict[t][0])
        sound2 = sound2 + intensityMap[t]
        sound1 = sound1.overlay(sound2)

    combinedSound = increaseDuration(sound1, 2)

    if not os.path.isdir(TEMP_FILES_PATH):
        os.mkdir(TEMP_FILES_PATH)
    combinedSound.export(TEMP_FILES_PATH + "/combinedSound.wav", format='wav')
    return combinedSound