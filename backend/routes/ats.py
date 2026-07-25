from fastapi import APIRouter
import os

from services.job_parser import JobParser
from services.resume_parser import ResumeParser
from services.skill_extractor import SkillExtractor
from services.ats_score import ATSScoreEngine

router = APIRouter(
    prefix="/ats",
    tags=["ATS Scoring"]
)

JOB_FOLDER = "uploads/jobs"

RESUME_FOLDER = "uploads/resumes"


@router.get("/")
def ats_score():

    job_files = os.listdir(JOB_FOLDER)

    if len(job_files) == 0:

        return {
            "error":"No Job Description Uploaded"
        }

    job_path = os.path.join(
        JOB_FOLDER,
        job_files[0]
    )

    job_text = JobParser.parse(job_path)

    required = SkillExtractor.extract(job_text)
    

    results = []

    for resume in os.listdir(RESUME_FOLDER):

        path = os.path.join(
            RESUME_FOLDER,
            resume
        )

        resume_text = ResumeParser.extract_text(path)

        candidate_skills = SkillExtractor.extract(resume_text)

        score = ATSScoreEngine.calculate(
            required,
            candidate_skills
        )

        results.append({

            "candidate": resume,

            **score

        })

    return results