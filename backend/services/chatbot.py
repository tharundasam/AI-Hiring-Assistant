class RecruiterChatbot:

    @staticmethod
    def answer(context, question):

        context_lower = context.lower()
        question = question.lower()

        if "python" in question:
            if "python" in context_lower:
                return "✅ Yes. The candidate has Python experience."
            return "❌ No Python experience was found."

        if "java" in question:
            if "java" in context_lower:
                return "✅ Yes. The candidate has Java experience."
            return "❌ No Java experience was found."

        if "aws" in question:
            if "aws" in context_lower:
                return "✅ Yes. The candidate has AWS experience."
            return "❌ No AWS experience was found."

        if "fastapi" in question:
            if "fastapi" in context_lower:
                return "✅ Yes. The candidate has FastAPI experience."
            return "❌ FastAPI experience was not found."

        if "skill" in question:
            return f"Skills found:\n\n{context}"

        if "summary" in question:
            return context

        if "experience" in question:
            return "Please review the experience section extracted from the resume."

        if "education" in question:
            return "Please review the education section extracted from the resume."

        if "project" in question:
            return "Please review the projects section extracted from the resume."

        return (
            "I couldn't understand the question. "
            "Try asking about Python, Java, AWS, FastAPI, skills, projects, education or experience."
        )


chatbot = RecruiterChatbot()