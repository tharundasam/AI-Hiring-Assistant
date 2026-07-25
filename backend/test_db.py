from database.db import SessionLocal
from models.resume import Resume

db = SessionLocal()

resume = Resume(
    filename="test.pdf",
    name="Test User",
    email="test@test.com",
    phone="9999999999",
    skills="Python",
    education="B.Tech",
    experience="1 Year",
    projects="AI Hiring",
    certifications="Microsoft",
    github="github.com/test",
    linkedin="linkedin.com/in/test",
    overall_score=90,
    semantic_score=88,
    matched_skills="Python",
    missing_skills="Docker",
    summary="Test Summary",
    interview_questions="Question 1"
)

db.add(resume)
db.commit()

print("Inserted!")

db.close()