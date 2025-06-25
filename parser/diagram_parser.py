# /parser/diagram_parser.py

import json
import re
from typing import List, Dict, Union


def clean_response(raw_response: str) -> Union[Dict, None]:
    """
    Attempt to extract JSON from GPT-4 raw response.
    GPT may return extra explanation text before or after the JSON.
    """
    try:
        # Find first and last curly braces to isolate JSON block
        json_start = raw_response.find('{')
        json_end = raw_response.rfind('}') + 1
        json_text = raw_response[json_start:json_end]
        return json.loads(json_text)
    except Exception:
        return None


def validate_step(step: Dict) -> bool:
    """Ensure the step dict has required keys and correct types."""
    required_keys = ['step_number', 'actor', 'action']
    if not all(key in step for key in required_keys):
        return False
    if not isinstance(step['step_number'], int):
        return False
    if not isinstance(step['actor'], str) or not isinstance(step['action'], str):
        return False
    return True


def is_decision(action: str) -> bool:
    return action.strip().endswith("?") or action.lower().startswith("is ")

def normalize_steps(raw_steps: List[Dict]) -> List[Dict]:
    cleaned = []
    for step in raw_steps:
        if validate_step(step):
            action_text = step["action"].strip()
            cleaned.append({
                "step_number": step["step_number"],
                "actor": step["actor"].strip(),
                "action": action_text,
                "condition": step.get("condition", "").strip(),
                "type": "decision" if is_decision(action_text) else "action"
            })
    return sorted(cleaned, key=lambda x: x['step_number'])


def parse_gpt_output(raw_response: str) -> Dict[str, Union[str, List[Dict]]]:
    """
    Full pipeline: Extracts JSON, validates and normalizes steps.
    Returns dict with 'summary' and 'steps'.
    """
    parsed = clean_response(raw_response)
    if not parsed or "steps" not in parsed or "summary" not in parsed:
        return {
            "summary": "Unable to extract valid summary.",
            "steps": []
        }

    normalized = normalize_steps(parsed["steps"])
    return {
        "summary": parsed["summary"].strip(),
        "steps": normalized
    }