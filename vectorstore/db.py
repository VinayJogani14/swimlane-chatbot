# /vectorstore/db.py

import faiss
import numpy as np
from typing import List
from vectorstore.embedder import get_embedder


class SwimlaneVectorDB:
    def __init__(self):
        self.embedder = get_embedder()
        self.index = faiss.IndexFlatL2(384)  # Match embedding dimension
        self.texts = []  # Embedded strings (actor + action + metadata)

    def add_documents(self, steps: List[dict]):
        texts = [
            f"{step.get('actor', '')}: {step.get('action', '')}"
            + (f" (Condition: {step.get('condition', '')})" if step.get('condition') else "")
            + (f" [Type: {step.get('type', 'action')}]" if step.get('type') else "")
            for step in steps
            if isinstance(step, dict) and step.get('actor') and step.get('action')
        ]

        if not texts:
            raise ValueError("No valid steps found to embed.")

        embeddings = self.embedder.embed_documents(texts)

        if not hasattr(embeddings, 'shape') or len(embeddings.shape) != 2 or embeddings.shape[0] == 0:
            raise ValueError(f"Embeddings must be 2D and non-empty. Got: {type(embeddings)}, value: {embeddings}")

        self.index.add(embeddings)
        self.texts.extend(texts)

    def search(self, query: str, top_k: int = 5):
        if self.index.ntotal == 0:
            raise ValueError("The index is empty. Add documents before searching.")

        query_embedding = self.embedder.embed_query(query)
        distances, indices = self.index.search(query_embedding, top_k)

        results = [self.texts[i] for i in indices[0] if i < len(self.texts)]
        return results