import faiss
import numpy as np


class FaissService:

    def __init__(self, dimension):

        self.index = faiss.IndexFlatL2(dimension)

        self.documents = []


    def add(self, embedding, metadata):

        embedding = np.array(
            [embedding],
            dtype="float32"
        )

        self.index.add(embedding)

        self.documents.append(metadata)


    def search(self, embedding, k=5):

        embedding = np.array(
            [embedding],
            dtype="float32"
        )

        distances, indices = self.index.search(
            embedding,
            k
        )

        results = []

        for distance, idx in zip(
            distances[0],
            indices[0]
        ):

            if idx != -1:

                results.append({

                    "distance": float(distance),

                    "metadata": self.documents[idx]

                })

        return results