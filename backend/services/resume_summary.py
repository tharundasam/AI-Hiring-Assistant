class ResumeSummary:

    @staticmethod
    def generate(
        name,
        matched_skills,
        missing_skills,
        overall_score,
        education_score,
        experience_score,
        projects_score,
        certification_score
    ):

        summary = []

        summary.append(
            f"{name} has an overall ATS score of {overall_score:.2f}%."
        )

        if matched_skills:
            summary.append(
                "Strong skills include "
                + ", ".join(matched_skills) + "."
            )

        if education_score >= 80:
            summary.append(
                "The candidate has a strong educational background."
            )

        if experience_score >= 80:
            summary.append(
                "Relevant experience matches the job requirements."
            )

        if projects_score >= 80:
            summary.append(
                "Projects demonstrate practical knowledge."
            )

        if certification_score >= 80:
            summary.append(
                "Professional certifications strengthen the profile."
            )

        if missing_skills:
            summary.append(
                "Recommended skills to learn: "
                + ", ".join(missing_skills) + "."
            )

        return " ".join(summary)