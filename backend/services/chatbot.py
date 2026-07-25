class RecruiterChatbot:

    @staticmethod
    def answer(context, question):

        question = question.lower()

        if "skill" in question:
            return "The candidate's skills are:\n\n" + context

        if "summary" in question:
            return context

        if "experience" in question:
            return "Please refer to the extracted experience section in the resume."

        if "education" in question:
            return "Please refer to the education details extracted from the resume."

        if "project" in question:
            return "The resume contains project information in the extracted projects section."

        return (
            "I couldn't find an exact answer. "
            "Please ask about skills, education, projects or experience."
        )


chatbot = RecruiterChatbot()