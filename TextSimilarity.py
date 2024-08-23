import os
import openai
import numpy as np
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
class TextSimilarity():
    def get_embedding(self, text):
        embedding = openai.Embedding.create(
                input=text,
                engine="text-embedding-ada-002"
            )['data'][0]['embedding']
        return embedding

    def cosine_similarity(self, vec1, vec2):
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        return dot_product / (norm_vec1 * norm_vec2)

    def calculate_similarity(self, text1, text2):
        embedding1 = self.get_embedding(text1)
        embedding2 = self.get_embedding(text2)
        
        similarity =self. cosine_similarity(embedding1, embedding2)
        return similarity

if __name__ == "__main__":
    text_similarity = TextSimilarity()
    score = text_similarity.calculate_similarity("hi", "hello")
    print(score)