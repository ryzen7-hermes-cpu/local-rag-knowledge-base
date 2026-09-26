from __future__ import annotations

from pathlib import Path
from typing import List

import chromadb
from sentence_transformers import SentenceTransformer

from knowledge_base_app.models import DocumentRecord


class VectorStore:
    def __init__(self, persist_directory: str | Path = "./chroma_db", embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"):
        self.persist_directory = str(persist_directory)
        self.embedding_model = embedding_model
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.collection = self.client.get_or_create_collection(name="knowledge_base")
        self.model = SentenceTransformer(embedding_model)

    def add_documents(self, documents: List[DocumentRecord]) -> None:
        if not documents:
            return

        texts = [doc.content for doc in documents]
        metadatas = [{"source": doc.source, "title": doc.title, **doc.metadata} for doc in documents]
        ids = [f"doc-{index}-{hash(doc.source + str(doc.metadata))}" for index, doc in enumerate(documents)]

        embeddings = self.model.encode(texts).tolist()
        self.collection.add(documents=texts, embeddings=embeddings, metadatas=metadatas, ids=ids)

    def similarity_search(self, query: str, k: int = 5) -> List[dict]:
        embedding = self.model.encode([query])[0].tolist()
        results = self.collection.query(query_embeddings=[embedding], n_results=k)

        matched = []
        for i in range(len(results.get("documents", [[]])[0])):
            matched.append({
                "content": results["documents"][0][i],
                "source": results["metadatas"][0][i].get("source"),
                "title": results["metadatas"][0][i].get("title"),
                "metadata": results["metadatas"][0][i],
            })
        return matched
