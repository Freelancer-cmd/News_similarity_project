import pandas as pd
import numpy as np
import pickle
import os
from pathlib import Path
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors


class NewsSearchEngine:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.documents = []
        self.metadata_path = Path("model/news_search_data")

    def create_embeddings(self, documents):
        """Generate embeddings for documents"""
        return self.model.encode(documents, convert_to_tensor=False).astype(np.float32)

    def build_index(self, embeddings):
        """Create and train the search index"""
        self.index = NearestNeighbors(n_neighbors=10, metric='cosine')
        self.index.fit(embeddings)

    def save_index(self):
        """Save index and metadata to disk"""
        self.metadata_path.mkdir(exist_ok=True)
        with open(self.metadata_path / "index.pkl", "wb") as f:
            pickle.dump(self.index, f)
        with open(self.metadata_path / "documents.pkl", "wb") as f:
            pickle.dump(self.documents, f)

    def load_index(self):
        """Load existing index from disk"""
        with open(self.metadata_path / "index.pkl", "rb") as f:
            self.index = pickle.load(f)
        with open(self.metadata_path / "documents.pkl", "rb") as f:
            self.documents = pickle.load(f)

    def search(self, query, top_k=10):
        """Search for similar news articles"""
        query_embedding = self.model.encode([query], convert_to_tensor=False).astype(np.float32)
        distances, indices = self.index.kneighbors(query_embedding)
        return [
            {
                "document": self.documents[idx],
                "distance": float(dist),
                "index": int(idx)
            }
            for dist, idx in zip(distances[0], indices[0])
        ]


# Example usage
if __name__ == "__main__":
    # Initialize search engine
    engine = NewsSearchEngine()

    # Build and save index (run once)
    if not os.path.exists("Data/news_search_data/index.pkl"):
        documents = engine.load_data("english_news_dataset.csv")
        embeddings = engine.create_embeddings(documents)
        engine.build_index(embeddings)
        engine.save_index()

    # Load existing index
    engine.load_index()

    # Perform search
    results = engine.search("violence against politicians", top_k=5)

    # Display results
    for i, result in enumerate(results):
        print(f"Result {i + 1}:")
        print(f"Distance: {result['distance']:.4f}")
        print(f"Content: {result['document'][:200]}...\n")
        print("-" * 80)