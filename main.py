from os import write
import os
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
import sys

from pydub import AudioSegment
import json

app = FastAPI()
IMAGE_DOWNLOAD_PATH = "uploadedImages/"
JSON_DICT_PATH = "databaseFiles/textMusicMapping.json"
INTENSITY_MAP_PATH = "databaseFiles/intensityMap.json"
SOUND_PATH = "databaseFiles/Dataset/audio/"
TEMP_FILES_PATH = "databaseFiles/tempFiles"


class UploadConfirmation(BaseModel):
    filename: str
    contenttype: str


@app.get("/")
def read_root():
    raise HTTPException(status_code=404, detail="Welcome! Not implemented yet :)")


@app.post("/upload/", response_model=UploadConfirmation)
async def upload(file: UploadFile = File(...)):
    if not os.path.isdir(IMAGE_DOWNLOAD_PATH):
        os.mkdir(IMAGE_DOWNLOAD_PATH)
    try:
        contents = await file.read()
        input_img_path = IMAGE_DOWNLOAD_PATH + os.sep + file.filename
        with open(input_img_path, 'wb') as f:
            f.write(contents)
    except Exception:
        e = sys.exc_info()[1]
        raise HTTPException(status_code=500, detail=str(e))

    # IMG2TXT

    # Tokenizer
    textArray = ["dog", "wind", "train"]

    # TXT2SOUND
    sound = textToSound(textArray)

    # SOUNDSYNTH
    # COMBINE IMAGE+SOUND
    # RETURN VIDEO REQUEST
    return {"filename": file.filename, "contenttype": file.content_type}


# --------------------------------------------------------Helpers
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
