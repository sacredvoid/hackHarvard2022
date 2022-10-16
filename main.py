import os
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
import sys
from gcp_helpers import download_blob, upload_blob
from sound_mapper_helpers import textToSound, addSoundToImage
from data import IMAGE_DOWNLOAD_PATH, GCP_BUCKET_NAME, TEMP_FILES_PATH, COMBINED_SOUND_FILENAME, \
    COMBINED_IMAGESOUND_FILENAME
from tokenizer import get_tokens
from img2text.image_to_text import predict_step

app = FastAPI()

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
        input_img_path = os.path.join(IMAGE_DOWNLOAD_PATH,file.filename)
        with open(input_img_path, 'wb') as f:
            f.write(contents)
        
    except Exception:
        e = sys.exc_info()[1]
        raise HTTPException(status_code=500, detail=str(e))

    # IMG2TXT
    text = predict_step([input_img_path])

    # Tokenizer
    
    textArray = get_tokens(text[0])
    print(textArray)
    # TXT2SOUND AND SOUNDSYNTH
    sound = textToSound(textArray)


    # COMBINE IMAGE+SOUND
    addSoundToImage(input_img_path, os.path.join(TEMP_FILES_PATH,COMBINED_SOUND_FILENAME),
                    os.path.join(TEMP_FILES_PATH,COMBINED_IMAGESOUND_FILENAME))
    # RETURN VIDEO REQUEST
    return {"filename": file.filename, "contenttype": file.content_type}


    # EXAMPLE GCP FUNCTIONS TO UPLOAD AND DOWNLOAD DATA
    # upload_blob(GCP_BUCKET_NAME,input_img_path)
    # download_blob(GCP_BUCKET_NAME, file.filename, './')