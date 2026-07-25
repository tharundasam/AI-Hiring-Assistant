from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
from services.skill_extractor import SkillExtractor
from services.information_extractor import InformationExtractor
from services.resume_parser import ResumeParser
from services.section_extractor import SectionExtractor
router = APIRouter(
    prefix="/upload",
    tags=["Resume Upload"]
)

UPLOAD_FOLDER = "uploads/resumes"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = [".pdf", ".docx"]


@router.post("/")
async def upload_resume(file: UploadFile = File(...)):

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed."
        )

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    extracted_text = ResumeParser.extract_text(filepath)

    skills = SkillExtractor.extract(extracted_text)

    email = InformationExtractor.extract_email(extracted_text)

    phone = InformationExtractor.extract_phone(extracted_text)

    name = InformationExtractor.extract_name(extracted_text)

    education = SectionExtractor.education(extracted_text)

    experience = SectionExtractor.experience(extracted_text)

    projects = SectionExtractor.projects(extracted_text)

    certifications = SectionExtractor.certifications(extracted_text)

    github = InformationExtractor.extract_github(extracted_text)

    linkedin = InformationExtractor.extract_linkedin(extracted_text)

    return {
        "filename": file.filename,
        "name": name,
        "email": email,
        "phone": phone,
        "skills": skills,
        "education": education,
        "experience": experience,
        "projects": projects,
        "certifications": certifications,
        "github": github,
        "linkedin": linkedin,
        "preview": extracted_text[:400]
    }