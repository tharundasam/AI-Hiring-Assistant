from fastapi import APIRouter, UploadFile, File
import os
import shutil

router = APIRouter(
    prefix="/job",
    tags=["Job Description"]
)

UPLOAD_FOLDER = "uploads/jobs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/")
async def upload_job(file: UploadFile = File(...)):

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "filename": file.filename,
        "message": "Job Description uploaded successfully.",
        "path": filepath
    }