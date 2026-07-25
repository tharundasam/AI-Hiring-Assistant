class InterviewQuestionGenerator:

    @staticmethod
    def generate(matched_skills, missing_skills):

        questions = {}

        skill_questions = {

            "python": [
                "Explain Python decorators.",
                "What is a generator in Python?",
                "Difference between list and tuple?"
            ],

            "java": [
                "Explain JVM architecture.",
                "Difference between HashMap and Hashtable.",
                "What is polymorphism?"
            ],

            "aws": [
                "Difference between EC2 and Lambda.",
                "Explain S3.",
                "What is IAM?"
            ],

            "sql": [
                "Write an INNER JOIN query.",
                "Explain normalization.",
                "Difference between WHERE and HAVING?"
            ],

            "azure": [
                "Explain Azure Virtual Machine.",
                "Difference between Azure Storage and Blob Storage."
            ],

            "typescript": [
                "Difference between interface and type.",
                "Explain Generics."
            ]
        }

        for skill in matched_skills:

            skill = skill.lower()

            if skill in skill_questions:
                questions[skill] = skill_questions[skill]

        if missing_skills:

            questions["Recommended Topics"] = []

            for skill in missing_skills:

                questions["Recommended Topics"].append(
                    f"Study {skill.title()} before the interview."
                )

        return questions