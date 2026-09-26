from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRecord:
    content: str
    source: str
    title: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)

    @property
    def id(self) -> str:
        return self.source


@dataclass
class DownloadConfig:
    target_dir: str
    source_type: str
    repo_owner: Optional[str] = None
    repo_name: Optional[str] = None
    url: Optional[str] = None
    branch: str = "main"
    include_patterns: Optional[List[str]] = None
