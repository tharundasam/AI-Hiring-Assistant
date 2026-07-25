import re


class SectionExtractor:

    @staticmethod
    def education(text):

        education_keywords = [
            "education",
            "academic",
            "qualification"
        ]

        lines = text.split("\n")

        collecting = False

        result = []

        for line in lines:

            line = line.strip()

            if line.lower() in education_keywords:
                collecting = True
                continue

            if collecting:

                if line == "":
                    break

                result.append(line)

        return result


    @staticmethod
    def experience(text):

        keywords = [
            "experience",
            "work experience",
            "professional experience"
        ]

        lines = text.split("\n")

        collecting = False

        result = []

        for line in lines:

            line = line.strip()

            if line.lower() in keywords:
                collecting = True
                continue

            if collecting:

                if line == "":
                    break

                result.append(line)

        return result


    @staticmethod
    def projects(text):

        keywords = [
            "projects",
            "project"
        ]

        lines = text.split("\n")

        collecting = False

        result = []

        for line in lines:

            line = line.strip()

            if line.lower() in keywords:

                collecting = True
                continue

            if collecting:

                if line == "":
                    break

                result.append(line)

        return result


    @staticmethod
    def certifications(text):

        keywords = [
            "certifications",
            "certificates"
        ]

        lines = text.split("\n")

        collecting = False

        result = []

        for line in lines:

            line = line.strip()

            if line.lower() in keywords:

                collecting = True
                continue

            if collecting:

                if line == "":
                    break

                result.append(line)

        return result