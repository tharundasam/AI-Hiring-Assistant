from sqlalchemy import Column, Integer, String, Float, Text

from database.db import Base


class Resume(Base):

    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String)
    name = Column(String)
    email = Column(String)
    phone = Column(String)

    skills = Column(Text)
    education = Column(Text)
    experience = Column(Text)
    projects = Column(Text)
    certifications = Column(Text)

    github = Column(String)
    linkedin = Column(String)

    overall_score = Column(Float)
    semantic_score = Column(Float)

    matched_skills = Column(Text)
    missing_skills = Column(Text)

    summary = Column(Text)

    interview_questions = Column(Text)