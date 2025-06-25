# /tests/test_openapi_parser.py

import os
import tempfile
import pytest
import yaml
import json
from openapi import parser

# Sample OpenAPI content (minimal)
OPENAPI_YAML = """
openapi: 3.0.0
info:
  title: Sample API
  version: 1.0.0
paths:
  /items:
    get:
      summary: Get items
      description: Returns a list of items.
      responses:
        '200':
          description: Successful response
"""

OPENAPI_JSON = {
    "openapi": "3.0.0",
    "info": {
        "title": "Sample API",
        "version": "1.0.0"
    },
    "paths": {
        "/products": {
            "post": {
                "summary": "Create product",
                "description": "Creates a new product entry.",
                "parameters": [
                    {
                        "name": "category",
                        "in": "query",
                        "description": "Product category",
                        "required": True
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Created successfully"
                    }
                }
            }
        }
    }
}


def test_load_openapi_spec_yaml():
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".yaml", delete=False) as f:
        f.write(OPENAPI_YAML)
        f.flush()
        loaded = parser.load_openapi_spec(f.name)
    assert "paths" in loaded
    os.remove(f.name)


def test_load_openapi_spec_json():
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as f:
        json.dump(OPENAPI_JSON, f)
        f.flush()
        loaded = parser.load_openapi_spec(f.name)
    assert "paths" in loaded
    os.remove(f.name)


def test_extract_and_convert_text_blocks():
    docs = parser.extract_endpoint_docs(OPENAPI_JSON)
    assert len(docs) == 1
    assert docs[0]["method"] == "POST"
    assert docs[0]["path"] == "/products"
    assert "parameters" in docs[0]
    
    text_blocks = parser.convert_to_text_blocks(docs)
    assert isinstance(text_blocks, list)
    assert "POST /products" in text_blocks[0]