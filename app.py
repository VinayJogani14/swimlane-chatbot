# /app.py

import streamlit as st
from dotenv import load_dotenv
import os

from utils.helpers import save_uploaded_file, validate_image
from utils.constants import SUPPORTED_IMAGE_TYPES
from llm.gpt4_vision import extract_from_image
from parser.diagram_parser import parse_gpt_output
from parser.sequence_generator import generate_sequence_text
from vectorstore.db import SwimlaneVectorDB
from chat.chatbot import answer_question
from openapi import parser as openapi_parser
from openapi import embedder as openapi_embedder

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Development Portal Chatbot", layout="wide")
st.title("🤖 Chatbot for Swimlane & API Understanding")

# Sidebar selection
st.sidebar.header("Upload Input File")
file_type = st.sidebar.radio("Select the type of input", ["Swimlane Diagram", "OpenAPI Spec"])

uploaded_file = st.sidebar.file_uploader("Upload a file", type=["png", "jpg", "jpeg", "json", "yaml", "yml"])

if uploaded_file:
    file_path = save_uploaded_file(uploaded_file)

    if file_type == "Swimlane Diagram":
        if not validate_image(file_path):
            st.error("Invalid image file.")
        else:
            with st.spinner("Analyzing swimlane diagram..."):
                raw_result = extract_from_image(file_path)
                parsed = parse_gpt_output(raw_result if isinstance(raw_result, str) else str(raw_result))

            st.subheader("🔎 Summary")
            st.markdown(parsed["summary"])

            st.subheader("📋 Extracted Steps")
            st.code(generate_sequence_text(parsed["steps"]), language="markdown")

            # Store to vector DB
            db = SwimlaneVectorDB()
            db.add_documents(parsed["steps"])

            st.session_state["swimlane_db"] = db
            st.session_state["parsed_steps"] = parsed["steps"]

            st.success("Diagram successfully parsed and indexed!")

    elif file_type == "OpenAPI Spec":
        try:
            with st.spinner("Parsing OpenAPI spec..."):
                spec = openapi_parser.load_openapi_spec(file_path)
                docs = openapi_parser.extract_endpoint_docs(spec)
                text_blocks = openapi_parser.convert_to_text_blocks(docs)
                openapi_embedder.index_openapi_spec(text_blocks)

            st.success(f"Parsed and indexed {len(text_blocks)} endpoint(s).")
            if st.checkbox("Show Parsed Endpoints"):
                for block in text_blocks:
                    st.code(block, language="markdown")

        except Exception as e:
            st.error(f"❌ Failed to parse OpenAPI file: {e}")

# Question interface
st.markdown("---")
st.subheader("💬 Ask a Question")

user_query = st.text_input("Enter your question about the uploaded flow or API:")

if user_query:
    with st.spinner("Thinking..."):
        response = answer_question(user_query)
        st.markdown(f"**Answer:** {response}")