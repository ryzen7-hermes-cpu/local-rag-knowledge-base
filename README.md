# Local RAG Knowledge Base

This project builds a local document knowledge base using a Retrieval-Augmented Generation (RAG) pipeline and a local LLM.

It can:
- download GitHub repositories
- fetch OpenAI / Anthropic / DeepSeek docs
- scrape arbitrary web pages
- ingest local Markdown and text documents
- embed and index content with local embeddings
- answer questions with Ollama-hosted local models
- operate via CLI or Streamlit web UI

## Features

- GitHub repo downloader
- OpenAI docs downloader
- Anthropic docs downloader
- DeepSeek docs downloader
- generic web page scraper
- local vector search with Chroma
- local embeddings via sentence-transformers
- local chat using Ollama
- multi-source knowledge base indexing

## Setup

### 1) Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

### 2) Install and run Ollama

```bash
ollama pull mistral
ollama serve
```

### 3) Download a source

```bash
python -m knowledge_base_app.cli download github --owner github --repo docs --target ./kb_data/github_docs
python -m knowledge_base_app.cli download openai --target ./kb_data/openai_docs
python -m knowledge_base_app.cli download anthropic --target ./kb_data/anthropic_docs
python -m knowledge_base_app.cli download deepseek --target ./kb_data/deepseek_docs
```

### 4) Ingest the documents

```bash
python -m knowledge_base_app.cli ingest --source-dir ./kb_data
```

### 5) Ask questions

```bash
python -m knowledge_base_app.cli chat --source-dir ./kb_data --model mistral
```

### 6) Launch the web app

```bash
streamlit run app.py
```

## Example

```python
from knowledge_base_app.rag_chat import RAGChatbot

bot = RAGChatbot(model_name="mistral", kb_dir="./kb_data")
bot.initialize()
print(bot.ask("How do I configure an API key?"))
```

## Repository structure

```text
.
├── app.py
├── README.md
├── requirements.txt
├── pyproject.toml
├── src/
│   └── knowledge_base_app/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── document_pipeline.py
│       ├── downloaders/
│       │   ├── __init__.py
│       │   ├── anthropic.py
│       │   ├── base.py
│       │   ├── deepseek.py
│       │   ├── github.py
│       │   ├── openai.py
│       │   └── web.py
│       ├── local_llm.py
│       ├── models.py
│       ├── rag_chat.py
│       └── vector_store.py
├── tests/
│   └── test_basic.py
└── kb_data/
```

## License

MIT
