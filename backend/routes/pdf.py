from fastapi import APIRouter
from fastapi.responses import FileResponse

from database.db import SessionLocal
from models.resume import Resume
from services.pdf_generator import PDFGenerator

router = APIRouter(
    prefix="/pdf",
    tags=["PDF"]
)

@router.get("/{resume_id}")
def generate_pdf(resume_id: int):

    db = SessionLocal()

    resume = db.query(Resume).filter(
        Resume.id == resume_id
    ).first()

    db.close()

    if not resume:
        return {"error": "Candidate not found"}

    candidate = {
        "name": resume.name,
        "email": resume.email,
        "phone": resume.phone,
        "skills": resume.skills,
        "education": resume.education,
        "experience": resume.experience,
        "projects": resume.projects,
        "certifications": resume.certifications,
        "overall_score": resume.overall_score,
        "semantic_score": resume.semantic_score,
        "summary": resume.summary,
        "interview_questions": resume.interview_questions,
    }

    filename = PDFGenerator.generate(candidate)

    return FileResponse(
        filename,
        media_type="application/pdf",
        filename=filename
    )