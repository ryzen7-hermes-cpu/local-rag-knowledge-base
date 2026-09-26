from __future__ import annotations

import argparse
from pathlib import Path

from knowledge_base_app.config import settings
from knowledge_base_app.downloaders import AnthropicDownloader, DeepSeekDownloader, GitHubDownloader, OpenAIDownloader, WebDownloader
from knowledge_base_app.rag_chat import RAGChatbot


def cmd_download(args):
    target = Path(args.target or "./kb_data")
    target.mkdir(parents=True, exist_ok=True)

    if args.source == "github":
        downloader = GitHubDownloader(target, owner=args.owner, repo=args.repo, branch=args.branch)
        return downloader.download()

    if args.source == "openai":
        downloader = OpenAIDownloader(target, url=args.url or settings.openai_url)
        return downloader.download()

    if args.source == "anthropic":
        downloader = AnthropicDownloader(target, url=args.url or settings.anthropic_url)
        return downloader.download()

    if args.source == "deepseek":
        downloader = DeepSeekDownloader(target, url=args.url or settings.deepseek_url)
        return downloader.download()

    if args.source == "web":
        downloader = WebDownloader(target, url=args.url)
        return downloader.download()

    raise ValueError(f"Unsupported source: {args.source}")


def cmd_ingest(args):
    source_dir = Path(args.source_dir or settings.kb_root)
    chatbot = RAGChatbot(model_name=args.model, kb_dir=source_dir)
    chatbot.initialize()
    if chatbot.ready:
        print(f"Successfully indexed knowledge base in {source_dir}")
    else:
        print(f"No documents found in {source_dir}")


def cmd_chat(args):
    chatbot = RAGChatbot(model_name=args.model, kb_dir=args.source_dir or settings.kb_root)
    chatbot.initialize()
    if not chatbot.ready:
        print("No documents indexed. Try running ingest first.")
        return
    chatbot.chat_loop()


def build_parser():
    parser = argparse.ArgumentParser(description="Local RAG knowledge base chatbot")
    subparsers = parser.add_subparsers(dest="command", required=True)

    download_parser = subparsers.add_parser("download", help="download docs from a source")
    download_parser.add_argument("source", choices=["github", "openai", "anthropic", "deepseek", "web"])
    download_parser.add_argument("--owner", default=None)
    download_parser.add_argument("--repo", default=None)
    download_parser.add_argument("--branch", default="main")
    download_parser.add_argument("--url", default=None)
    download_parser.add_argument("--target", default="./kb_data")
    download_parser.set_defaults(func=cmd_download)

    ingest_parser = subparsers.add_parser("ingest", help="index documents into the local vector store")
    ingest_parser.add_argument("--source-dir", default="./kb_data")
    ingest_parser.add_argument("--model", default=settings.default_model)
    ingest_parser.set_defaults(func=cmd_ingest)

    chat_parser = subparsers.add_parser("chat", help="start interactive chat")
    chat_parser.add_argument("--source-dir", default="./kb_data")
    chat_parser.add_argument("--model", default=settings.default_model)
    chat_parser.set_defaults(func=cmd_chat)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
