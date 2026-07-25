import re
class ATSScoreEngine:


    @staticmethod
    def calculate(
        semantic_score,
        required_skills,
        candidate_skills,
        education,
        experience,
        projects,
        certifications
    ):

        # ---------- Skills ----------

        matched = []

        missing = []

        for skill in required_skills:

            if skill in candidate_skills:
                matched.append(skill)
            else:
                missing.append(skill)

        if len(required_skills):

            skills_score = (
                len(matched) /
                len(required_skills)
            ) * 100

        else:

            skills_score = 100

        # ---------- Education ----------

        education_score = 100 if education else 0

        # ---------- Experience ----------

        experience_score = 100 if experience else 0

        # ---------- Projects ----------

        projects_score = 100 if projects else 0

        # ---------- Certifications ----------

        certification_score = 100 if certifications else 0

        overall = (

            semantic_score * 0.40 +

            skills_score * 0.30 +

            education_score * 0.10 +

            experience_score * 0.10 +

            projects_score * 0.05 +

            certification_score * 0.05

        )

        return {

            "overall_score": round(overall,2),

            "semantic_score": round(semantic_score,2),

            "skills_score": round(skills_score,2),

            "education_score": education_score,

            "experience_score": experience_score,

            "projects_score": projects_score,

            "certification_score": certification_score,

            "matched_skills": matched,

            "missing_skills": missing

        }