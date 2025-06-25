# /tests/test_diagram_parser.py

import pytest
from parser.diagram_parser import parse_gpt_output, validate_step, normalize_steps

# Mock GPT response (as a string)
MOCK_RAW_RESPONSE = """
{
  "summary": "This diagram represents a basic order processing workflow.",
  "steps": [
    {
      "step_number": 1,
      "actor": "Customer",
      "action": "Places an order"
    },
    {
      "step_number": 2,
      "actor": "Sales",
      "action": "Validates the order",
      "condition": "If stock is available"
    },
    {
      "step_number": 3,
      "actor": "Finance",
      "action": "Processes payment"
    }
  ]
}
"""

def test_parse_gpt_output_structure():
    result = parse_gpt_output(MOCK_RAW_RESPONSE)
    assert isinstance(result, dict)
    assert "summary" in result
    assert "steps" in result
    assert isinstance(result["steps"], list)
    assert result["summary"].startswith("This diagram")

def test_validate_step_good():
    good_step = {
        "step_number": 1,
        "actor": "User",
        "action": "Clicks a button"
    }
    assert validate_step(good_step) is True

def test_validate_step_missing_fields():
    bad_step = {
        "step_number": 2,
        "action": "Submits a form"
    }
    assert validate_step(bad_step) is False

def test_normalize_steps_ordering():
    unordered = [
        {"step_number": 3, "actor": "C", "action": "Third"},
        {"step_number": 1, "actor": "A", "action": "First"},
        {"step_number": 2, "actor": "B", "action": "Second"}
    ]
    normalized = normalize_steps(unordered)
    assert normalized[0]["step_number"] == 1
    assert normalized[1]["step_number"] == 2
    assert normalized[2]["step_number"] == 3