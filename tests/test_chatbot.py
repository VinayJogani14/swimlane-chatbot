# /tests/test_chatbot.py

import pytest
from unittest.mock import patch
from chat import chatbot

# Mock search result
MOCK_CONTEXT_RESULTS = [
    ({
        "step_number": 1,
        "actor": "Customer",
        "action": "Submits an order",
        "condition": ""
    }, 0.9),
    ({
        "step_number": 2,
        "actor": "Sales",
        "action": "Verifies order",
        "condition": "If inventory is available"
    }, 0.85)
]

@patch("chat.chatbot.SwimlaneVectorDB")
def test_retrieve_context(mock_db_class):
    mock_db = mock_db_class.return_value
    mock_db.search.return_value = MOCK_CONTEXT_RESULTS
    
    context = chatbot.retrieve_context("Who verifies the order?")
    
    assert "Customer - Submits an order" in context
    assert "Sales - Verifies order" in context
    assert "Condition: If inventory is available" in context


@patch("chat.chatbot.openai.ChatCompletion.create")
@patch("chat.chatbot.SwimlaneVectorDB")
def test_answer_question(mock_db_class, mock_gpt):
    mock_db = mock_db_class.return_value
    mock_db.search.return_value = MOCK_CONTEXT_RESULTS
    
    mock_gpt.return_value = {
        "choices": [{
            "message": {
                "content": "The Sales team verifies the order if inventory is available."
            }
        }]
    }

    answer = chatbot.answer_question("Who verifies the order?")
    
    assert "Sales team verifies the order" in answer
    mock_gpt.assert_called_once()