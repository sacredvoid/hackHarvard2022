import os
from fastapi import FastAPI, HTTPException, File, Request, UploadFile
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import sys

from pydub import AudioSegment

from gcp_helpers import upload_blob
from post_req_helper import send_post
from sound_mapper_helpers import textToSound, addSoundToImage, increaseDuration
from data import IMAGE_DOWNLOAD_PATH, GCP_BUCKET_NAME, TEMP_FILES_PATH, COMBINED_SOUND_FILENAME, \
    COMBINED_IMAGESOUND_FILENAME, NOISE_FILE_PATH, IMG2TEXT_API
from tokenizer import get_tokens

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class UploadConfirmation(BaseModel):
    filename: str
    contenttype: str

@app.get("/")
def main(request: Request):
    # textlink
    videolink = "https://storage.googleapis.com/audio-data-hack/combinedImageSound.mp4"
    input = ""
    # heatmaplink
    # animationlink
    return templates.TemplateResponse("index.html", {"request": request, "input":input, "video":videolink})

@app.post("/upload/", response_model=UploadConfirmation)
async def upload(file: UploadFile = File(...)):
    if not os.path.isdir(IMAGE_DOWNLOAD_PATH):
        os.mkdir(IMAGE_DOWNLOAD_PATH)
    try:
        contents = await file.read()
        input_img_path = os.path.join(IMAGE_DOWNLOAD_PATH,file.filename)
        with open(input_img_path, 'wb') as f:
            f.write(contents)
        
        input_img_path1 = os.path.join(IMAGE_DOWNLOAD_PATH, "inputimage.jpg")
        with open(input_img_path1, 'wb') as f:
            f.write(contents)
        
    except Exception:
        e = sys.exc_info()[1]
        raise HTTPException(status_code=500, detail=str(e))
    
    # move to api call
    text = send_post(IMG2TEXT_API, input_img_path)
    # Tokenizer
    textArray = get_tokens(text)
    
    # TXT2SOUND AND SOUNDSYNTH
    sound = textToSound(textArray)
    if sound == -1:
        sound1 = AudioSegment.from_file(NOISE_FILE_PATH + "noise.wav")
        combinedSound = increaseDuration(sound1, 2)
        if not os.path.isdir(TEMP_FILES_PATH):
            os.mkdir(TEMP_FILES_PATH)
        combinedSound.export(TEMP_FILES_PATH + COMBINED_SOUND_FILENAME, format='wav')

    # COMBINE IMAGE+SOUND
    addSoundToImage(input_img_path, os.path.join(TEMP_FILES_PATH , COMBINED_SOUND_FILENAME),
                    os.path.join(TEMP_FILES_PATH, COMBINED_IMAGESOUND_FILENAME))


    # UPLOAD TO CLOUD
    upload_blob(GCP_BUCKET_NAME, os.path.join(TEMP_FILES_PATH, COMBINED_IMAGESOUND_FILENAME))
    upload_blob(GCP_BUCKET_NAME, IMAGE_DOWNLOAD_PATH + "inputimage.jpg")

    # FIND HEAT MAP AND UPLOAD TO CLOUD
    # MAKE ANIMATION AND UPLOAD TO CLOUD

    # DELETE AUDIO
    os.remove(TEMP_FILES_PATH + COMBINED_SOUND_FILENAME)

    # RETURN VIDEO REQUEST
    return {"filename": file.filename, "contenttype": file.content_type}