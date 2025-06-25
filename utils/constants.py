# /utils/constants.py

# Embedding Models
DEFAULT_EMBEDDING_MODEL = "all-MiniLM-L6-v2"
OPENAI_EMBEDDING_MODEL = "text-embedding-3-small"

# GPT Models
GPT4_VISION_MODEL = "gpt-4-vision-preview"
GPT4_TEXT_MODEL = "gpt-4"

# File types
SUPPORTED_IMAGE_TYPES = [".png", ".jpg", ".jpeg"]
SUPPORTED_SPEC_TYPES = [".yaml", ".yml", ".json"]

# Upload Directories
UPLOAD_IMAGE_DIR = "data/uploads"
UPLOAD_SPEC_DIR = "data/specs"

# Vector DB Parameters
EMBEDDING_DIM = 384  # For MiniLM

# System Prompts
SYSTEM_PROMPT_SWIMLANE = """
You are a business process analyst. Analyze the uploaded swimlane diagram and return:
1. A short summary of the process.
2. A structured list of steps in JSON:
   [{step_number, actor, action, condition}]
"""

SYSTEM_PROMPT_API_DOC = """
You are a technical documentation assistant. Given OpenAPI 3.0 specs, help the user understand endpoints,
parameters, and responses in simple terms using only the retrieved context.
"""