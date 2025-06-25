# /vectorstore/embedder.py

import os
import numpy as np
from typing import List, Union
from sentence_transformers import SentenceTransformer

# Load env settings
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "local").lower()
OPENAI_EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


class LocalEmbedder:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed_documents(self, texts: List[str]) -> np.ndarray:
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        print(f"[Embedder] Local embeddings shape: {embeddings.shape}")
        return embeddings

    def embed_query(self, query: str) -> np.ndarray:
        return self.embed_documents([query]).reshape(1, -1)


class OpenAIEmbedder:
    def __init__(self):
        from openai import OpenAI
        self.client = OpenAI()
        self.model = OPENAI_EMBEDDING_MODEL

    def embed_documents(self, texts: List[str]) -> np.ndarray:
        embeddings = []
        for text in texts:
            response = self.client.embeddings.create(
                input=text,
                model=self.model
            )
            vector = response.data[0].embedding
            embeddings.append(vector)
        arr = np.array(embeddings)
        print(f"[Embedder] OpenAI embeddings shape: {arr.shape}")
        return arr

    def embed_query(self, query: str) -> np.ndarray:
        return self.embed_documents([query]).reshape(1, -1)


def get_embedder() -> Union[LocalEmbedder, OpenAIEmbedder]:
    if EMBEDDING_PROVIDER == "openai":
        print("[Embedder] Using OpenAI Embeddings")
        return OpenAIEmbedder()
    else:
        print("[Embedder] Using Local Embeddings (MiniLM)")
        return LocalEmbedder()