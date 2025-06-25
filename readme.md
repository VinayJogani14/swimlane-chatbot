# 🧠 Swimlane & OpenAPI-Aware Chatbot

A domain-specific chatbot capable of parsing and understanding Swimlane Diagrams (unstructured images) and OpenAPI 3.0 specifications (structured data), built to support development portal documentation, accelerate onboarding, and enhance process transparency.

> Built using GPT-4 Vision + local embeddings + FAISS vector search.  

---

## Features

- Upload and parse **Swimlane diagrams** (images)
- Extract **structured step sequences** from images using GPT‑4 Vision
- Parse **OpenAPI specs** (YAML or JSON) into searchable endpoint blocks
- Embed parsed content using **MiniLM (local)** or OpenAI embeddings
- Use **GPT‑4o** for domain-specific, contextual Q&A
- Supports questions like:
  - *"Who cancels the order?"*
  - *"What does POST /orders do?"*
  - *"How many actors are in this workflow?"*

## 📁 Project Structure

chatbot-swimlane-app/
│
├── app.py                        # Main Streamlit app
├── chat/
│   └── chatbot.py               # GPT-powered Q&A logic
│
├── llm/
│   └── gpt4_vision.py           # Extracts content from diagrams via GPT-4 Vision
│
├── openapi/
│   ├── parser.py                # Loads & parses OpenAPI 3.0 specs
│   └── embedder.py              # Embeds OpenAPI text blocks
│
├── parser/
│   ├── diagram_parser.py        # Parses GPT output into structured steps
│   └── sequence_generator.py    # Converts steps into human-readable Markdown
│
├── utils/
│   ├── constants.py
│   ├── helpers.py
│
├── vectorstore/
│   ├── db.py                    # FAISS vector DB
│   └── embedder.py             # Embedding logic (MiniLM or OpenAI)
│
└── .env                         # API Keys

---

## 🧪 How It Works

### 1. **Upload a Diagram or API Spec**
- `.png`, `.jpg`, `.jpeg` for Swimlanes
- `.yaml`, `.yml`, `.json` for OpenAPI

### 2. **Parsing Logic**
- **Swimlanes**: Processed using `gpt-4-vision`, converted to JSON steps
- **OpenAPI Specs**: Parsed using `PyYAML`, summarized into endpoint docs

### 3. **Embedding & Indexing**
- Uses **MiniLM (`all-MiniLM-L6-v2`)** via `SentenceTransformer`
- Embeddings stored in **FAISS** for fast vector search

### 4. **Answering Questions**
- Relevant context retrieved
- GPT‑4o composes answers based only on indexed context

---

## 🔧 Setup Instructions

### Requirements

- Python 3.9+
- OpenAI API Key (if using GPT‑4 Vision or OpenAI Embeddings)

### Installation

```bash
git clone https://github.com/vinayjogani14/swimlane-chatbot.git
cd swimlane-openapi-chatbot
python -m venv venv
source venv/bin/activate   # or venv\Scripts\activate on Windows

pip install -r requirements.txt

Set Environment Variables

Create a .env file:

OPENAI_API_KEY=sk-xxxx...

----

📚 References
	•	GPT-4 Vision: https://openai.com/index/gpt-4/
	•	MiniLM Sentence Transformers: https://www.sbert.net/docs/sentence_transformer/pretrained_models.html
	•	FAISS for vector search: https://github.com/facebookresearch/faiss
	•	OpenAPI Spec: https://swagger.io/specification/
⸻

🧑‍💻 Author

Vinay Jogani 

---