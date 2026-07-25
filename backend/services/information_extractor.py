import re
import spacy

nlp = spacy.load("en_core_web_sm")


class InformationExtractor:

    @staticmethod
    def extract_email(text):

        pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

        match = re.search(pattern, text)

        if match:
            return match.group()

        return ""


    @staticmethod
    def extract_phone(text):

        pattern = r"(\+?\d[\d\s\-]{8,}\d)"

        match = re.search(pattern, text)

        if match:
            return match.group()

        return ""


    @staticmethod
    def extract_name(text):

        doc = nlp(text[:1000])

        for ent in doc.ents:

            if ent.label_ == "PERSON":

                return ent.text

        return ""

    @staticmethod
    def extract_github(text):

        pattern = r"https?://github\.com/[A-Za-z0-9_.-]+"

        match = re.search(pattern, text)

        if match:
            return match.group()

        return ""


    @staticmethod
    def extract_linkedin(text):

        pattern = r"https?://(www\.)?linkedin\.com/in/[A-Za-z0-9_-]+"

        match = re.search(pattern, text)

        if match:
            return match.group()

        return ""