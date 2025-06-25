# Swimlane & OpenAPI-Aware Chatbot

A domain-specific chatbot that can intelligently parse and understand both **Swimlane Diagrams** (unstructured images) and **OpenAPI 3.0 Specifications** (structured YAML/JSON).  
It is designed to support development portal documentation, accelerate onboarding, and improve process transparency by enabling contextual, conversational access to backend workflows and APIs.

> Powered by GPT-4 Vision + MiniLM Embeddings + FAISS Vector Search + Streamlit UI

---

## Features

- Upload and parse **Swimlane diagrams** (image-based process flows)
- Extract structured **step-by-step sequences** using GPT‑4 Vision
- Upload **OpenAPI specs** (YAML or JSON) for structured endpoint extraction
- Automatically embed and index both structured and unstructured data
- Ask domain-specific questions and receive contextual responses using **GPT‑4o**
- Example Questions:
  - "Who cancels the order?"
  - "What does `POST /orders` do?"
  - "How many actors are in this workflow?"
  - "What fields are required to create a new order?"

---

## Project Structure

chatbot-swimlane-app/
│
├── app.py                     # Main Streamlit app entry point
│
├── chat/
│   └── chatbot.py             # Handles question-answering using embeddings and GPT
│
├── llm/
│   └── gpt4_vision.py         # Uses GPT-4 Vision API to extract structured steps from images
│
├── openapi/
│   ├── parser.py              # Parses OpenAPI YAML/JSON and generates text docs
│   └── embedder.py            # Embeds OpenAPI documentation blocks for search
│
├── parser/
│   ├── diagram_parser.py      # Converts GPT vision output to structured steps
│   └── sequence_generator.py  # Formats steps into human-readable sequences
│
├── utils/
│   ├── constants.py
│   ├── helpers.py             # Helpers for file I/O, validation, etc.
│
├── vectorstore/
│   ├── db.py                  # FAISS-based vector DB implementation
│   └── embedder.py            # Embedding logic using SentenceTransformer or OpenAI
│
└── .env                       # Secrets (e.g., OPENAI_API_KEY)

---

## How It Works

### 1. **Upload a File**
- **Swimlane Diagrams**: `.png`, `.jpg`, `.jpeg`
- **OpenAPI Specs**: `.yaml`, `.yml`, `.json`

### 2. **Parsing**
- **Swimlanes**: GPT‑4 Vision processes the image and extracts a sequence of structured steps (`actor`, `action`, `decision`, etc.)
- **OpenAPI**: YAML/JSON specs are parsed into human-readable endpoint descriptions

### 3. **Embedding & Indexing**
- Embeddings are generated using:
  - `all-MiniLM-L6-v2` (via `SentenceTransformer`) for local embeddings
- Stored in an in-memory **FAISS** index for fast similarity search

### 4. **Question Answering**
- When a question is asked:
  - Relevant indexed steps/docs are retrieved
  - GPT‑4o uses them as context to generate domain-specific answers

---

## Setup Instructions

### Requirements
- Python 3.9+
- OpenAI API Key (for GPT‑4 Vision + GPT-4o)

### Installation

git clone https://github.com/vinayjogani14/swimlane-chatbot.git
cd swimlane-chatbot
python -m venv venv
source venv/bin/activate     # or venv\Scripts\activate on Windows
pip install -r requirements.txt

Environment Variables

Create a .env file in the root:

OPENAI_API_KEY=sk-xxxx...


⸻

References
	•	GPT-4 Vision: https://openai.com/index/gpt-4/
	•	MiniLM Sentence Transformers: https://www.sbert.net/docs/sentence_transformer/pretrained_models.html
	•	FAISS for Vector Search: https://github.com/facebookresearch/faiss
	•	OpenAPI Specification: https://swagger.io/specification/
	•	Streamlit: https://streamlit.io/

⸻

�Author

Vinay Jogani

