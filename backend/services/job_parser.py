from services.resume_parser import ResumeParser


class JobParser:

    @staticmethod
    def parse(filepath):

        return ResumeParser.extract_text(filepath)