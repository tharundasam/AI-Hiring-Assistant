from sentence_transformers import SentenceTransformer

class EmbeddingService:

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    @staticmethod
    def generate_embedding(text):

        embedding = EmbeddingService.model.encode(
            text,
            convert_to_numpy=True
        )

        return embedding