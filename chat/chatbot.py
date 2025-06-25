# /chat/chatbot.py

import os
import streamlit as st
from openai import OpenAI
from vectorstore.db import SwimlaneVectorDB

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def retrieve_context(query: str, top_k: int = 20):
    """
    Searches the vector database for relevant steps and extracts metadata.

    Returns:
        - context string
        - list of unique actors
        - list of decision steps
    """
    db = st.session_state.get("swimlane_db")
    if db is None:
        print("[Chatbot] No swimlane DB in session.")
        return "", [], []

    try:
        results = db.search(query, top_k=top_k)
    except ValueError as e:
        print(f"[Chatbot] Skipping context retrieval: {e}")
        return "", [], []

    context_blocks = []
    actor_set = set()
    decision_steps = []

    for text in results:
        context_blocks.append(f"- {text}")
        if ":" in text:
            actor, action = text.split(":", 1)
            actor_set.add(actor.strip())
            if "?" in action.strip():
                decision_steps.append(action.strip())

    return "\n".join(context_blocks), sorted(actor_set), decision_steps


def answer_question(query: str) -> str:
    """
    Answers user question using GPT-4 with vector search context and extracted metadata.
    """
    context, actors, decision_steps = retrieve_context(query)

    system_prompt = (
        "You are a business process assistant. Use the provided context from a swimlane diagram "
        "to answer the user's question accurately. Do not make assumptions beyond the context."
    )

    extra_facts = ""
    if actors:
        extra_facts += f"\nActors involved: {', '.join(actors)}."
    if decision_steps:
        extra_facts += f"\nDetected decision steps: {len(decision_steps)} such as:\n" + "\n".join(decision_steps[:3])

    if context:
        user_prompt = f"{extra_facts}\n\nContext:\n{context}\n\nQuestion:\n{query}"
    else:
        user_prompt = f"{extra_facts}\n\nQuestion:\n{query}"

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3,
        max_tokens=500
    )

    return response.choices[0].message.content.strip()