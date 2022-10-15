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
    try:
        contents = await file.read()
    except Exception:
        e = sys.exc_info()[1]
        raise HTTPException(status_code=500, detail=str(e))

    return {"filename": file.filename, "contenttype":file.content_type}