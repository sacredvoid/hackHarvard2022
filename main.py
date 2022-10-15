from os import write
import os
from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel
import sys

app = FastAPI()
IMAGE_DOWNLOAD_PATH = "uploaded_images/"

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
        input_img_path = IMAGE_DOWNLOAD_PATH+os.sep+file.filename
        with open(input_img_path,'wb') as f:
            f.write(contents)
    except Exception:
        e = sys.exc_info()[1]
        raise HTTPException(status_code=500, detail=str(e))

    # IMG2TXT
    # Tokenizer
    # TXT2SOUND
    # SOUNDSYNTH
    # COMBINE IMAGE+SOUND
    # RETURN VIDEO REQUEST
    return {"filename": file.filename, "contenttype":file.content_type}