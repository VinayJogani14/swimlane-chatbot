# /llm/gpt4_vision.py

import base64
import json
from config import OPENAI_API_KEY
from openai import OpenAI

# Initialize OpenAI client using key from config
client = OpenAI(api_key=OPENAI_API_KEY)

def extract_from_image(image_path: str) -> dict:
    """
    Sends an image of a swim lane diagram to GPT-4 Vision and returns a structured response.

    Returns:
        dict: {
            "summary": str,
            "steps": list of dicts [
                {
                    "step_number": int,
                    "actor": str,
                    "action": str,
                    "condition": Optional[str]
                },
                ...
            ]
        }
    """
    # Read and encode image to base64
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    base64_image = base64.b64encode(image_data).decode("utf-8")
    image_url = f"data:image/png;base64,{base64_image}"

    # Call GPT-4 Vision
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert business analyst. Given a swim lane diagram image, "
                    "extract and return a structured description of the workflow in JSON format. "
                    "Include two fields:\n"
                    "1. summary: a brief overview of the process\n"
                    "2. steps: a list of step-by-step actions as [{step_number, actor, action, condition_if_any}]"
                )
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Please analyze this swim lane diagram and return the structured JSON."},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ],
        max_tokens=1000,
        temperature=0.4
    )

    result_text = response.choices[0].message.content
    return result_text 