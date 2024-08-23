from transformers import ViTModel
from transformers import ViTFeatureExtractor
from PIL import Image
import chromadb
import os
from sklearn.metrics.pairwise import cosine_similarity

class ImgSearcher():
    def __init__(self):
        model_save_path = 'model'
        feature_extractor_save_path = 'feature_extractor'
        self.model = ViTModel.from_pretrained(model_save_path)
        self.feature_extractor = ViTFeatureExtractor.from_pretrained(feature_extractor_save_path)
        self.chroma_client = chromadb.PersistentClient(path='data/chroma2.db')
        self.collection = self.chroma_client.get_or_create_collection(name='img', metadata={"hnsw:space": "cosine"})

    def get_embeddings(self, img_path):
        image = Image.open(img_path)
        inputs = self.feature_extractor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state[:, 0, :]
        return embeddings.tolist()
    
    def add_img(self, img_path):
        embeddings = self.get_embeddings(img_path)
        id = os.path.splitext(img_path)[0]
        self.collection.add(embeddings=embeddings, documents=[img_path], ids=[f"id_{id}"])
    
    def query(self, img_path, n_results):
        embeddings = self.get_embeddings(img_path)
        res = self.collection.query(query_embeddings=embeddings, n_results=n_results)
        
        return res
    
    def get_cosine_similarity(self, img1, img2):
        embeddings1 = self.get_embeddings(img1)
        embeddings2 = self.get_embeddings(img2)
        return cosine_similarity(embeddings1, embeddings2)

if __name__ == "__main__":
    imgSearcher = ImgSearcher()
    print(imgSearcher.get_cosine_similarity('data/train/asparagus1_resized.jpeg', 'data/train/asparagus2_resized.jpg'))
    print(imgSearcher.query('data/train/asparagus1_resized.jpeg', n_results=40))

