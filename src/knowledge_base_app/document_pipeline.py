from __future__ import annotations

from pathlib import Path
from typing import Iterable, List
import re

from knowledge_base_app.models import DocumentRecord


def normalize_space(text: str) -> str:
    text = text.replace("\r", "\n")
    text = text.replace("\t", " ")
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


def read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="replace")


def load_local_documents(source_dir: str | Path) -> List[DocumentRecord]:
    source_dir = Path(source_dir)
    documents: List[DocumentRecord] = []

    if not source_dir.exists():
        return documents

    for path in sorted(source_dir.rglob("*")):
        if path.is_dir():
            continue
        if path.suffix.lower() not in {".md", ".txt", ".html", ".htm"}:
            continue

        text = read_text_file(path)
        if not text.strip():
            continue

        documents.append(
            DocumentRecord(
                content=normalize_space(text),
                source=str(path),
                title=path.name,
                metadata={"file": str(path)},
            )
        )

    return documents


def chunk_text(text: str, chunk_size: int = 800, overlap: int = 120) -> List[str]:
    paragraphs = re.split(r"\n{2,}", text)
    chunks: List[str] = []
    current = ""

    for para in paragraphs:
        para = normalize_space(para)
        if not para:
            continue

        if len(current) + len(para) <= chunk_size:
            current = (current + "\n\n" + para).strip()
        else:
            if current:
                chunks.append(current)
            if len(para) > chunk_size:
                pieces = [para[i:i + chunk_size] for i in range(0, len(para), chunk_size - overlap)]
                for piece in pieces:
                    if piece.strip():
                        chunks.append(piece.strip())
                current = ""
            else:
                current = para

    if current:
        chunks.append(current)

    return chunks


def prepare_documents(documents: Iterable[DocumentRecord], chunk_size: int = 800, overlap: int = 120) -> List[DocumentRecord]:
    prepared: List[DocumentRecord] = []
    for doc in documents:
        chunks = chunk_text(doc.content, chunk_size=chunk_size, overlap=overlap)
        for index, chunk in enumerate(chunks):
            prepared.append(
                DocumentRecord(
                    content=chunk,
                    source=doc.source,
                    title=doc.title or Path(doc.source).name,
                    metadata={**doc.metadata, "chunk_index": index},
                )
            )

    return prepared
