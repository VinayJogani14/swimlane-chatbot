# /openapi/embedder.py

from typing import List
import numpy as np
from vectorstore.embedder import get_embedder
from vectorstore.db import SwimlaneVectorDB

# Initialize shared embedder instance (local or OpenAI)
embedder = get_embedder()

# Shared DB instance for OpenAPI spec chunks
openapi_db = SwimlaneVectorDB()

def embed_openapi_chunks(chunks: List[str]) -> np.ndarray:
    """
    Embeds OpenAPI chunks using the selected embedding provider.
    
    Args:
        chunks: List of text segments (e.g., endpoint summaries).
        
    Returns:
        np.ndarray: 2D array of shape (n_chunks, embedding_dim)
    """
    if not chunks:
        raise ValueError("No chunks provided for embedding.")
    
    print(f"[OpenAPI Embedder] Embedding {len(chunks)} chunks...")
    return embedder.embed_documents(chunks)

def index_openapi_spec(text_blocks: List[str]):
    """
    Embeds and indexes OpenAPI endpoint text blocks into a vector database.
    
    Args:
        text_blocks: List of endpoint descriptions or summaries.
    """
    if not text_blocks:
        raise ValueError("No OpenAPI text blocks provided for indexing.")
    
    print(f"[OpenAPI Embedder] Indexing {len(text_blocks)} blocks into vector DB...")
    documents = [{"actor": "API", "action": block} for block in text_blocks]
    openapi_db.add_documents(documents)
    
    import streamlit as st
    st.session_state["openapi_db"] = openapi_db