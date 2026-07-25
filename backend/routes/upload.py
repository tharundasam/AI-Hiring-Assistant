from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
from services.skill_extractor import SkillExtractor
from services.information_extractor import InformationExtractor
from services.resume_parser import ResumeParser
from services.section_extractor import SectionExtractor
from database.db import SessionLocal
from models.resume import Resume
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

    print("1. Upload endpoint called")

    extracted_text = ResumeParser.extract_text(filepath)

    print("2. Text extracted")

    skills = SkillExtractor.extract(extracted_text)

    print("3. Skills extracted")

    email = InformationExtractor.extract_email(extracted_text)

    phone = InformationExtractor.extract_phone(extracted_text)

    name = InformationExtractor.extract_name(extracted_text)

    print("4. Personal information extracted")

    education = SectionExtractor.education(extracted_text)

    experience = SectionExtractor.experience(extracted_text)

    projects = SectionExtractor.projects(extracted_text)

    certifications = SectionExtractor.certifications(extracted_text)

    print("5. Resume sections extracted")

    github = InformationExtractor.extract_github(extracted_text)

    linkedin = InformationExtractor.extract_linkedin(extracted_text)

    print("6. GitHub & LinkedIn extracted")

    db = SessionLocal()

    db = SessionLocal()
    print("7. Database session created")

    try:
        print("========== DATABASE INSERT ==========")

        resume = Resume(
            filename=file.filename,
            name=name,
            email=email,
            phone=phone,
            skills=", ".join(skills) if isinstance(skills, list) else str(skills),
            education=education,
            experience=experience,
            projects=projects,
            certifications=certifications,
            github=github,
            linkedin=linkedin,
            overall_score=0.0,
            semantic_score=0.0,
            matched_skills="",
            missing_skills="",
            summary="",
            interview_questions=""
        )

        print("8. About to insert into database")

        db.add(resume)
        db.commit()

        print("9. Database committed successfully")
        db.refresh(resume)

        print(f"10. Resume inserted with ID: {resume.id}")

    except Exception as e:
        db.rollback()
        print("❌ DATABASE ERROR")
        print(type(e).__name__)
        print(str(e))

    finally:
        db.close()

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