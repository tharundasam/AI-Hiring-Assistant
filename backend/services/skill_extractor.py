import re
import spacy

nlp = spacy.load("en_core_web_sm")


SKILL_DATABASE = {

    "python",
    "java",
    "c",
    "c++",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "fastapi",
    "flask",
    "django",
    "streamlit",
    "pytorch",
    "tensorflow",
    "keras",
    "scikit-learn",
    "pandas",
    "numpy",
    "matplotlib",
    "opencv",
    "docker",
    "kubernetes",
    "aws",
    "azure",
    "gcp",
    "git",
    "github",
    "linux",
    "react",
    "nodejs",
    "html",
    "css",
    "javascript",
    "typescript",
    "power bi",
    "tableau"
}


class SkillExtractor:

    @staticmethod
    def extract(text):

        text = text.lower()

        found = []

        for skill in SKILL_DATABASE:

            if re.search(r"\b" + re.escape(skill) + r"\b", text):

                found.append(skill)

        return sorted(list(set(found)))