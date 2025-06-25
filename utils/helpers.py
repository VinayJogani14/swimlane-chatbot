# /utils/helpers.py

import os
import uuid
from PIL import Image
from typing import Tuple
import base64

UPLOAD_DIR = "data/uploads"

def save_uploaded_file(uploaded_file) -> str:
    """
    Save uploaded image file to a local directory with a unique name.

    Args:
        uploaded_file (streamlit UploadedFile): The uploaded file object.

    Returns:
        str: Local file path.
    """
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_ext = os.path.splitext(uploaded_file.name)[-1]
    unique_name = f"{uuid.uuid4().hex}{file_ext}"
    save_path = os.path.join(UPLOAD_DIR, unique_name)

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return save_path


def validate_image(path: str) -> bool:
    """
    Ensure the uploaded file is a valid image.

    Args:
        path (str): File path.

    Returns:
        bool: True if valid image.
    """
    try:
        Image.open(path).verify()
        return True
    except Exception:
        return False


def encode_image_base64(path: str) -> str:
    """
    Convert image to base64 for GPT-4 Vision API.

    Args:
        path (str): Local image file path.

    Returns:
        str: Base64-encoded image string (for data:image/... usage).
    """
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    mime_type = "image/png" if path.lower().endswith(".png") else "image/jpeg"
    return f"data:{mime_type};base64,{encoded}"