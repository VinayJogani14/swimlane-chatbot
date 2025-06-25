# /config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# === API Keys ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
if not OPENAI_API_KEY:
    raise ValueError("Missing OPENAI_API_KEY in environment variables or .env")

# === Embedding Configuration ===
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "local").lower()  # 'local' or 'openai'
EMBEDDING_MODEL_NAME = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")

# === Upload Directories ===
UPLOAD_IMAGE_DIR = os.getenv("UPLOAD_IMAGE_DIR", "data/uploads")
UPLOAD_SPEC_DIR = os.getenv("UPLOAD_SPEC_DIR", "data/specs")

# === Model Names ===
GPT4_VISION_MODEL = "gpt-4-vision-preview"
GPT4_TEXT_MODEL = "gpt-4"

# === Vector DB Configuration ===
VECTOR_DIMENSION = 384  # All-MiniLM-L6-v2 default

# === Other Settings ===
TOP_K_RETRIEVAL = int(os.getenv("TOP_K_RETRIEVAL", 5))