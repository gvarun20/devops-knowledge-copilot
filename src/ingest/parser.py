"""Parse Kubernetes + Terraform documentation into JSONL."""

from __future__ import annotations

import json
import re
from pathlib import Path

import frontmatter

from src.config import load_settings, root_path
from src.models import Document

SHORTCODE = re.compile(r"\{\{<\s*[^>]+\s*>\}\}|\{\{%\s*[^%]+\s*%\}\}")
HTML_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
MDX_IMPORT = re.compile(r"^import\s+.+$", re.MULTILINE)


def clean_text(text: str) -> str:
    text = SHORTCODE.sub("", text)
    text = HTML_COMMENT.sub("", text)
    text = MDX_IMPORT.sub("", text)
    return text.strip()


def source_url(tool: str, path: Path, base: str) -> str:
    posix = path.as_posix()
    if tool == "kubernetes":
        m = re.search(r"content/en/docs/(.+)\.md$", posix)
        if m:
            return f"{base}/{m.group(1).replace('_index', '').rstrip('/')}/"
    if tool == "terraform":
        m = re.search(r"content/terraform/[^/]+/docs/(.+)\.mdx$", posix)
        if m:
            return f"{base}/{m.group(1).replace('/index', '').rstrip('/')}"
    return base


def parse_repo(tool: str, repo: Path, pattern: str, base_url: str) -> list[Document]:
    docs: list[Document] = []
    for path in sorted(repo.glob(pattern)):
        post = frontmatter.loads(path.read_text(encoding="utf-8", errors="ignore"))
        body = clean_text(post.content)
        if len(body.split()) < 20:
            continue
        title = post.get("page_title") or post.get("title") or path.stem
        docs.append(
            Document(
                tool=tool,
                title=str(title),
                file_path=path.relative_to(repo).as_posix(),
                source_url=source_url(tool, path, base_url),
                content=body,
                word_count=len(body.split()),
            )
        )
    return docs


def save_jsonl(docs: list[Document], out: Path) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        for doc in docs:
            f.write(doc.model_dump_json() + "\n")


def load_jsonl(path: Path) -> list[Document]:
    docs: list[Document] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            docs.append(Document.model_validate_json(line))
    return docs


def run_ingestion() -> None:
    settings = load_settings()
    paths = settings["paths"]
    all_docs: list[Document] = []

    for key in ("kubernetes", "terraform"):
        src = settings["doc_sources"][key]
        repo = root_path(paths[f"raw_{key}"])
        if not repo.exists():
            raise FileNotFoundError(f"Missing {repo}. Run scripts/01_setup_data.py first.")
        batch = parse_repo(src["tool"], repo, src["content_glob"], src["docs_base_url"])
        print(f"{key}: {len(batch)} documents")
        all_docs.extend(batch)

    out = root_path(paths["processed_documents"])
    save_jsonl(all_docs, out)
    print(f"Saved {len(all_docs)} documents -> {out}")
