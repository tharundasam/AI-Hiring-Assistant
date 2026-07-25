from fpdf import FPDF

class PDFGenerator:

    @staticmethod
    def generate(candidate):

        pdf = FPDF()

        pdf.add_page()

        pdf.set_font("Arial", "B", 16)
        pdf.cell(190, 10, "AI Hiring Assistant Report", ln=True)

        pdf.ln(5)

        pdf.set_font("Arial", "", 12)

        pdf.multi_cell(0, 8, f"Name: {candidate['name']}")
        pdf.multi_cell(0, 8, f"Email: {candidate['email']}")
        pdf.multi_cell(0, 8, f"Phone: {candidate['phone']}")

        pdf.ln(3)

        pdf.multi_cell(0, 8, f"Skills:\n{candidate['skills']}")

        pdf.ln(3)

        pdf.multi_cell(0, 8, f"Education:\n{candidate['education']}")

        pdf.ln(3)

        pdf.multi_cell(0, 8, f"Experience:\n{candidate['experience']}")

        pdf.ln(3)

        pdf.multi_cell(0, 8, f"Projects:\n{candidate['projects']}")

        pdf.ln(3)

        pdf.multi_cell(0, 8, f"Certifications:\n{candidate['certifications']}")

        pdf.ln(3)

        pdf.multi_cell(
            0,
            8,
            f"ATS Score: {candidate['overall_score']}"
        )

        pdf.multi_cell(
            0,
            8,
            f"Semantic Score: {candidate['semantic_score']}"
        )

        pdf.ln(3)

        pdf.multi_cell(
            0,
            8,
            f"AI Summary:\n{candidate['summary']}"
        )

        pdf.ln(3)

        pdf.multi_cell(
            0,
            8,
            f"Interview Questions:\n{candidate['interview_questions']}"
        )

        filename = f"{candidate['name']}.pdf"

        pdf.output(filename)

        return filename