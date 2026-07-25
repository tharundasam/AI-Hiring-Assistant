import pdfplumber
from docx import Document
import os


class ResumeParser:

    @staticmethod
    def extract_text(file_path: str):

        extension = os.path.splitext(file_path)[1].lower()

        if extension == ".pdf":
            return ResumeParser.extract_pdf(file_path)

        elif extension == ".docx":
            return ResumeParser.extract_docx(file_path)

        elif extension == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()

        else:
            raise ValueError("Unsupported file format")


    @staticmethod
    def extract_pdf(file_path):

        text = ""

        with pdfplumber.open(file_path) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

        return text


    @staticmethod
    def extract_docx(file_path):

        document = Document(file_path)

        text = ""

        for paragraph in document.paragraphs:

            text += paragraph.text + "\n"

        return text