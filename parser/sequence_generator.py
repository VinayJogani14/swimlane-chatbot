# /parser/sequence_generator.py

from typing import List, Dict


def generate_sequence_text(steps: List[Dict]) -> str:
    """
    Convert a list of structured step dicts into a human-readable, linear sequence.
    
    Args:
        steps (List[Dict]): List of step objects with step_number, actor, action, condition.

    Returns:
        str: Text summary describing the process in sequential order.
    """
    lines = []
    for step in sorted(steps, key=lambda x: x["step_number"]):
        line = f"Step {step['step_number']}: {step['actor']} performs '{step['action']}'"
        if step.get("condition"):
            line += f" (Condition: {step['condition']})"
        lines.append(line)

    return "\n".join(lines)


def get_step_chunks(steps: List[Dict], chunk_size: int = 5) -> List[str]:
    """
    Converts the list of steps into semantically grouped text chunks for vector DB.
    Useful if steps list is long.

    Args:
        steps (List[Dict]): List of cleaned step dicts.
        chunk_size (int): Number of steps per chunk.

    Returns:
        List[str]: List of text blocks, each representing a chunk of steps.
    """
    chunks = []
    for i in range(0, len(steps), chunk_size):
        group = steps[i:i + chunk_size]
        chunk_text = generate_sequence_text(group)
        chunks.append(chunk_text)
    return chunks