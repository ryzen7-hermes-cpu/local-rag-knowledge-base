from __future__ import annotations

from pathlib import Path

from knowledge_base_app.models import DocumentRecord


class BaseDownloader:
    source_name = "base"

    def __init__(self, target_dir: str | Path, **kwargs):
        self.target_dir = Path(target_dir)
        self.target_dir.mkdir(parents=True, exist_ok=True)

    def download(self):
        raise NotImplementedError


class GitHubDownloader(BaseDownloader):
    source_name = "github"

    def __init__(self, target_dir: str | Path, owner: str, repo: str, branch: str = "main", **kwargs):
        super().__init__(target_dir)
        self.owner = owner
        self.repo = repo
        self.branch = branch
        self.url = f"https://github.com/{owner}/{repo}.git"

    def download(self):
        target_path = self.target_dir / self.repo
        if target_path.exists():
            return [DocumentRecord(content=f"Repository already exists at {target_path}", source=str(target_path), title=self.repo)]

        import subprocess
        subprocess.run(["git", "clone", "--depth", "1", "--branch", self.branch, self.url, str(target_path)], check=True)
        return [DocumentRecord(content=f"Downloaded {self.owner}/{self.repo}", source=str(target_path), title=self.repo)]


class OpenAIDownloader(BaseDownloader):
    source_name = "openai"

    def __init__(self, target_dir: str | Path, url: str = "https://platform.openai.com/docs", **kwargs):
        super().__init__(target_dir)
        self.url = url

    def download(self):
        import requests
        from bs4 import BeautifulSoup
        response = requests.get(self.url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        text = "\n".join(p.get_text(" ", strip=True) for p in soup.find_all(["p", "h1", "h2", "h3", "li"]))
        out_file = self.target_dir / "openai_docs.txt"
        out_file.write_text(text, encoding="utf-8")
        return [DocumentRecord(content=text, source=str(out_file), title="OpenAI docs")]


class AnthropicDownloader(BaseDownloader):
    source_name = "anthropic"

    def __init__(self, target_dir: str | Path, url: str = "https://docs.anthropic.com/en", **kwargs):
        super().__init__(target_dir)
        self.url = url

    def download(self):
        import requests
        from bs4 import BeautifulSoup
        response = requests.get(self.url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        text = "\n".join(p.get_text(" ", strip=True) for p in soup.find_all(["p", "h1", "h2", "h3", "li"]))
        out_file = self.target_dir / "anthropic_docs.txt"
        out_file.write_text(text, encoding="utf-8")
        return [DocumentRecord(content=text, source=str(out_file), title="Anthropic docs")]


class DeepSeekDownloader(BaseDownloader):
    source_name = "deepseek"

    def __init__(self, target_dir: str | Path, url: str = "https://api-docs.deepseek.com/", **kwargs):
        super().__init__(target_dir)
        self.url = url

    def download(self):
        import requests
        from bs4 import BeautifulSoup
        response = requests.get(self.url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        text = "\n".join(p.get_text(" ", strip=True) for p in soup.find_all(["p", "h1", "h2", "h3", "li"]))
        out_file = self.target_dir / "deepseek_docs.txt"
        out_file.write_text(text, encoding="utf-8")
        return [DocumentRecord(content=text, source=str(out_file), title="DeepSeek docs")]


class WebDownloader(BaseDownloader):
    source_name = "web"

    def __init__(self, target_dir: str | Path, url: str, **kwargs):
        super().__init__(target_dir)
        self.url = url

    def download(self):
        import requests
        from bs4 import BeautifulSoup
        response = requests.get(self.url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        text = "\n".join(p.get_text(" ", strip=True) for p in soup.find_all(["p", "h1", "h2", "h3", "li"]))
        out_file = self.target_dir / "web_page.txt"
        out_file.write_text(text, encoding="utf-8")
        return [DocumentRecord(content=text, source=str(out_file), title="Web page")]
