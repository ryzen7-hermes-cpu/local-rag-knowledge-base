#!/usr/bin/env python3

from argparse import Namespace

from knowledge_base_app.cli import cmd_download


if __name__ == "__main__":
    args = Namespace(
        source="github",
        owner="github",
        repo="docs",
        branch="main",
        url=None,
        target="./kb_data/github_docs",
    )
    cmd_download(args)
    print("Downloaded GitHub docs example")
