# /tests/test_vectorstore.py

import os
import shutil
import pytest
from vectorstore.db import SwimlaneVectorDB

TEST_DATA_PATH = "data/faiss_index"
TEST_META_PATH = "data/faiss_metadata.pkl"

@pytest.fixture(autouse=True)
def cleanup_vectorstore():
    """Ensure vector store is cleaned before and after each test run."""
    yield
    if os.path.exists(TEST_DATA_PATH):
        os.remove(TEST_DATA_PATH)
    if os.path.exists(TEST_META_PATH):
        os.remove(TEST_META_PATH)

def test_add_and_search_documents():
    db = SwimlaneVectorDB()
    
    steps = [
        {
            "step_number": 1,
            "actor": "User",
            "action": "Logs into the portal",
            "condition": ""
        },
        {
            "step_number": 2,
            "actor": "System",
            "action": "Validates credentials",
            "condition": "If password is correct"
        }
    ]
    
    db.add_documents(steps)
    assert len(db.metadata) == 2
    
    results = db.search("Who validates credentials?")
    
    assert len(results) > 0
    assert isinstance(results[0][0], dict)
    assert "actor" in results[0][0]
    assert results[0][0]["actor"] in ["User", "System"]