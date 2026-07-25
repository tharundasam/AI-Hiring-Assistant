from fastapi import APIRouter
import os
from database.db import SessionLocal
from models.resume import Resume
from services.resume_parser import ResumeParser
from services.embedding import EmbeddingService
from services.similarity import SimilarityEngine
from services.skill_extractor import SkillExtractor
from services.section_extractor import SectionExtractor
from services.interview_generator import InterviewQuestionGenerator
from services.resume_summary import ResumeSummary
from services.ats_score import ATSScoreEngine
router = APIRouter(
    prefix="/ranking",
    tags=["Resume Ranking"]
)

RESUME_FOLDER = "uploads/resumes"
JOB_FOLDER = "uploads/jobs"


@router.get("/")
def rank_resumes():

    job_files = os.listdir(JOB_FOLDER)

    if not job_files:
        return {
            "error": "No Job Description uploaded."
        }

    job_path = os.path.join(
        JOB_FOLDER,
        job_files[0]
    )

    job_text = ResumeParser.extract_text(job_path)

    job_embedding = EmbeddingService.generate_embedding(
        job_text
    )

    required_skills = SkillExtractor.extract(job_text)

    results = []

    for filename in os.listdir(RESUME_FOLDER):

        filepath = os.path.join(
            RESUME_FOLDER,
            filename
        )

        resume_text = ResumeParser.extract_text(
            filepath
        )

        candidate_skills = SkillExtractor.extract(resume_text)

        education = SectionExtractor.education(resume_text)

        experience = SectionExtractor.experience(resume_text)

        projects = SectionExtractor.projects(resume_text)

        certifications = SectionExtractor.certifications(resume_text)

        resume_embedding = EmbeddingService.generate_embedding(
            resume_text
        )

        semantic = SimilarityEngine.calculate(
            job_embedding,
            resume_embedding
        ) * 100

        ats = ATSScoreEngine.calculate(
            semantic,
            required_skills,
            candidate_skills,
            education,
            experience,
            projects,
            certifications
        )

        summary = ResumeSummary.generate(
            filename,
            ats["matched_skills"],
            ats["missing_skills"],
            ats["overall_score"],
            ats["education_score"],
            ats["experience_score"],
            ats["projects_score"],
            ats["certification_score"]
        )

        questions = InterviewQuestionGenerator.generate(
            ats["matched_skills"],
            ats["missing_skills"]
        )

        db = SessionLocal()

        candidate = db.query(Resume).filter(
            Resume.filename == filename
        ).first()

        if candidate:

            candidate.overall_score = ats["overall_score"]

            candidate.semantic_score = semantic

            candidate.summary = summary

            candidate.matched_skills = ", ".join(
                ats["matched_skills"]
            )

            candidate.missing_skills = ", ".join(
                ats["missing_skills"]
            )

            candidate.interview_questions = "\n".join(
                questions
            )

            db.commit()

        db.close()
 
        results.append({
            "candidate": filename,
            **ats,
            "summary": summary,
            "interview_questions": questions
        })

    results.sort(
        key=lambda x: x["overall_score"],
        reverse=True
    )

    return {

        "total_candidates": len(results),

        "ranking": results

    }