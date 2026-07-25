from sklearn.metrics.pairwise import cosine_similarity


class SimilarityEngine:

    @staticmethod
    def calculate(job_embedding, resume_embedding):

        score = cosine_similarity(
            [job_embedding],
            [resume_embedding]
        )[0][0]

        return round(float(score), 4)