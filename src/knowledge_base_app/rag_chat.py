from __future__ import annotations

from pathlib import Path

from knowledge_base_app.config import settings
from knowledge_base_app.document_pipeline import load_local_documents, prepare_documents
from knowledge_base_app.local_llm import OllamaClient
from knowledge_base_app.vector_store import VectorStore


class RAGChatbot:
    def __init__(self, model_name: str | None = None, kb_dir: str | Path | None = None, vector_db_path: str | Path | None = None):
        self.model_name = model_name or settings.default_model
        self.kb_dir = Path(kb_dir) if kb_dir else settings.kb_root
        self.vector_db_path = Path(vector_db_path) if vector_db_path else settings.vector_db_path
        self.llm = OllamaClient(base_url=settings.ollama_base_url, model=self.model_name)
        self.vector_store = VectorStore(persist_directory=self.vector_db_path, embedding_model=settings.embedding_model)
        self.ready = False

    def initialize(self) -> None:
        docs = load_local_documents(self.kb_dir)
        if not docs:
            self.ready = False
            return

        prepared = prepare_documents(docs, chunk_size=settings.chunk_size, overlap=settings.chunk_overlap)
        self.vector_store.add_documents(prepared)
        self.ready = True

    def ask(self, question: str) -> str:
        if not self.ready:
            return "The knowledge base has not been initialized yet. Run initialize() or ingest first."

        results = self.vector_store.similarity_search(question, k=settings.max_retrieved_docs)
        context = "\n\n".join(f"Source: {item['source']}\n{item['content']}" for item in results)

        prompt = f"""
You are a helpful assistant using the following knowledge base. Use the context when possible. If the answer is missing, say so clearly.

Context:
{context}

User question:
{question}

Answer directly and mention relevant source files if helpful.
""".strip()

        return self.llm.generate(prompt)

    def chat_loop(self) -> None:
        print("Knowledge base assistant ready. Type 'quit' to exit.")
        while True:
            question = input("You: ").strip()
            if question.lower() in {"quit", "exit", "q"}:
                break
            if not question:
                continue
            print("Assistant:")
            print(self.ask(question))
            print()
