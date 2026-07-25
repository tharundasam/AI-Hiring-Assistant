from fastapi import APIRouter, UploadFile, File
import os
import shutil

from database.db import SessionLocal
from models.job import Job

router = APIRouter(
    prefix="/job",
    tags=["Job"]
)

UPLOAD_FOLDER = "uploads/jobs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/")
async def upload_job(file: UploadFile = File(...)):

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Read text if TXT
    description = ""

    if file.filename.endswith(".txt"):
        with open(filepath, "r", encoding="utf-8") as f:
            description = f.read()

    db = SessionLocal()

    job = Job(
        filename=file.filename,
        description=description
    )

    db.add(job)
    db.commit()
    db.refresh(job)
    db.close()

    return {
        "message": "Job Uploaded",
        "job_id": job.id
    }