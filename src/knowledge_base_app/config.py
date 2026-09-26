from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import os
from typing import Optional


@dataclass
class Settings:
    project_root: Path = field(default_factory=lambda: Path(__file__).resolve().parents[2])
    kb_root: Path = field(default_factory=lambda: Path(os.getenv("KB_ROOT", "./kb_data")))
    vector_db_path: Path = field(default_factory=lambda: Path(os.getenv("VECTOR_DB_PATH", "./chroma_db")))
    default_model: str = os.getenv("OLLAMA_MODEL", "mistral")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "800"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "120"))
    max_retrieved_docs: int = int(os.getenv("MAX_RETRIEVED_DOCS", "5"))
    docs_root: Path = field(default_factory=lambda: Path(os.getenv("DOCS_ROOT", "./kb_data")))
    openai_url: str = os.getenv("OPENAI_DOCS_URL", "https://platform.openai.com/docs")
    anthropic_url: str = os.getenv("ANTHROPIC_DOCS_URL", "https://docs.anthropic.com/en")
    deepseek_url: str = os.getenv("DEEPSEEK_DOCS_URL", "https://api-docs.deepseek.com/")
    github_token: Optional[str] = os.getenv("GITHUB_TOKEN")


settings = Settings()
