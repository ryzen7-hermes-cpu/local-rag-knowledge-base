from __future__ import annotations

import streamlit as st

from knowledge_base_app.config import settings
from knowledge_base_app.rag_chat import RAGChatbot

st.set_page_config(page_title="Local KB Chat", page_icon="📚")

if "chatbot" not in st.session_state:
    st.session_state.chatbot = RAGChatbot(model_name=settings.default_model, kb_dir=settings.kb_root)
    st.session_state.chatbot.initialize()

st.title("📚 Local Knowledge Base Assistant")

if not st.session_state.chatbot.ready:
    st.warning("No documents are indexed yet. Put files into ./kb_data or run the CLI ingest command.")

question = st.text_input("Ask a question about your knowledge base")

if question:
    with st.spinner("Searching the knowledge base..."):
        answer = st.session_state.chatbot.ask(question)
    st.markdown(answer)
