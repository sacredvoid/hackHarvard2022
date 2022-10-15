import json
import os
from pydub import AudioSegment

from gcp_helpers import download_blob
from data import SOUND_PATH, JSON_DICT_PATH, TEMP_FILES_PATH, INTENSITY_MAP_PATH, GCP_BUCKET_NAME, \
    COMBINED_SOUND_FILENAME, JSON_FILENAME, INTENSITY_MAP_FILENAME
import pandas as pd
import json
import random
from moviepy.editor import AudioFileClip, ImageClip




def increaseDuration(sound, factor):
    for i in range(0, factor):
        sound = sound.append(sound, crossfade=400)
    return sound


def textToSound(textArray):
    filePath = SOUND_PATH

    # Open JSON file to dictionary.
    # fetch from API ///////////////////////////////////////////////////////////
    download_blob(GCP_BUCKET_NAME, JSON_DICT_PATH+JSON_FILENAME, './')
    jsonFileName = JSON_DICT_PATH + JSON_FILENAME
    with open(jsonFileName) as json_file:
        jsonDict = json.load(json_file)

    # Set loudness based on intensity map
    # fetch from API ///////////////////////////////////////////////////////////
    download_blob(GCP_BUCKET_NAME, INTENSITY_MAP_PATH+INTENSITY_MAP_FILENAME, './')
    jsonFileName = INTENSITY_MAP_PATH + INTENSITY_MAP_FILENAME
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
    combinedSound.export(TEMP_FILES_PATH + COMBINED_SOUND_FILENAME, format='wav')
    return combinedSound

def addSoundToImage(imagePath, audioPath, outputPath):
    audio_clip = AudioFileClip(audioPath)
    image_clip = ImageClip(imagePath)
    video_clip = image_clip.set_audio(audio_clip)
    video_clip.duration = audio_clip.duration
    video_clip.fps = 1
    video_clip.write_videofile(outputPath)


# Create Json file
def createTextSoundJson(filePath):
    # Import excel
    df = pd.read_csv(filePath)

    # Create Json
    jsonDict = {}
    for index, row in df.iterrows():
        if row['category'] not in jsonDict.keys():
            jsonDict[row['category']] = []
        jsonDict[row['category']].append(row['filename'])

    # Dump json
    with open(JSON_DICT_PATH, "w") as fp:
        json.dump(jsonDict, fp, indent=4)

    """
    # Dump unique text names
    with open(TEMP_FILES_PATH, "w") as fp:
        for line in jsonDict.keys():
            fp.write(line + '\n')
    """


def updateJson(inputDict):
    jsonFileName = JSON_DICT_PATH
    with open(jsonFileName) as json_file:
        jsonDict = json.load(json_file)

    for v in inputDict:
        if v in jsonDict.keys():
            jsonDict[v].append(inputDict[v])
        else:
            jsonDict[v] = []
            jsonDict[v].append(inputDict[v])


# Create intensity map
def createIntensityMap(csvFilePath):
    df = pd.read_csv(csvFilePath)

    # Create Json
    jsonDict = {}
    for index, row in df.iterrows():
        if row['category'] not in jsonDict.keys():
            jsonDict[row['category']] = random.randint(-5, 0)

    # Dump json
    with open(INTENSITY_MAP_PATH, "w") as fp:
        json.dump(jsonDict, fp, indent=4)
