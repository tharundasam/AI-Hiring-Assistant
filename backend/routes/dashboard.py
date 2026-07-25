from fastapi import APIRouter
from database.db import SessionLocal
from models.resume import Resume

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/")
def get_dashboard():

    db = SessionLocal()

    resumes = db.query(Resume).order_by(
        Resume.overall_score.desc()
    ).all()

    result = []

    for r in resumes:
        result.append({
            "id": r.id,
            "name": r.name,
            "email": r.email,
            "phone": r.phone,
            "skills": r.skills,
            "education": r.education,
            "experience": r.experience,
            "projects": r.projects,
            "certifications": r.certifications,
            "summary": r.summary,
            "interview_questions": r.interview_questions,
            "overall_score": r.overall_score,
            "semantic_score": r.semantic_score
        })

    db.close()

    return result