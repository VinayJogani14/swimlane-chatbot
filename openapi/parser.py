# /openapi/parser.py

import json
import yaml
from typing import Union, List, Dict


def load_openapi_spec(file_path: str) -> Dict:
    """
    Load an OpenAPI spec from a JSON or YAML file.

    Args:
        file_path (str): Path to the OpenAPI spec file.

    Returns:
        dict: Parsed OpenAPI schema.
    """
    with open(file_path, 'r') as f:
        if file_path.endswith(".json"):
            return json.load(f)
        elif file_path.endswith(".yaml") or file_path.endswith(".yml"):
            return yaml.safe_load(f)
        else:
            raise ValueError("Unsupported file type. Use .json or .yaml")


def extract_endpoint_docs(spec: Dict) -> List[Dict]:
    """
    Extract endpoint documentation from OpenAPI spec.

    Returns:
        List[Dict]: List of endpoints with method, path, summary, parameters, etc.
    """
    docs = []
    paths = spec.get("paths", {})

    for path, methods in paths.items():
        for method, operation in methods.items():
            if not isinstance(operation, dict):
                continue

            doc = {
                "method": method.upper(),
                "path": path,
                "summary": operation.get("summary", ""),
                "description": operation.get("description", ""),
                "parameters": [],
                "responses": []
            }

            # Parameters
            for param in operation.get("parameters", []):
                doc["parameters"].append({
                    "name": param.get("name", ""),
                    "in": param.get("in", ""),
                    "description": param.get("description", ""),
                    "required": param.get("required", False)
                })

            # Responses
            for code, resp in operation.get("responses", {}).items():
                doc["responses"].append({
                    "code": code,
                    "description": resp.get("description", "")
                })

            docs.append(doc)

    return docs


def convert_to_text_blocks(docs: List[Dict]) -> List[str]:
    """
    Convert structured endpoint docs into readable text for embedding.

    Returns:
        List[str]: List of text chunks.
    """
    chunks = []
    for d in docs:
        chunk = f"{d['method']} {d['path']}\nSummary: {d['summary']}\nDescription: {d['description']}\n"

        if d["parameters"]:
            chunk += "Parameters:\n"
            for p in d["parameters"]:
                chunk += f"  - {p['name']} ({p['in']}): {p['description']} [Required: {p['required']}]\n"

        if d["responses"]:
            chunk += "Responses:\n"
            for r in d["responses"]:
                chunk += f"  - {r['code']}: {r['description']}\n"

        chunks.append(chunk.strip())

    return chunks