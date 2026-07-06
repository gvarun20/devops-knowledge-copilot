"""Header-aware chunking."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path

from src.config import load_settings, root_path
from src.models import Chunk, Document

HEADER = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)


def chunk_id(tool: str, path: str, header: str, index: int) -> str:
    raw = f"{tool}|{path}|{header}|{index}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def split_sections(text: str) -> list[tuple[str, list[str], str]]:
    matches = list(HEADER.finditer(text))
    if not matches:
        return [("Document", ["Document"], text)]

    sections: list[tuple[str, list[str], str]] = []
    stack: list[tuple[int, str]] = []

    for i, match in enumerate(matches):
        level = len(match.group(1))
        header = match.group(2).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()

        while stack and stack[-1][0] >= level:
            stack.pop()
        stack.append((level, header))
        path = [h for _, h in stack]
        sections.append((header, path, body))

    return sections


def word_windows(text: str, size: int, overlap: int) -> list[str]:
    words = text.split()
    if len(words) <= size:
        return [text] if text else []
    step = max(size - overlap, 1)
    return [" ".join(words[i : i + size]) for i in range(0, len(words), step)]


def chunk_document(doc: Document) -> list[Chunk]:
    cfg = load_settings()["chunking"]
    target = cfg["target_words"]
    max_words = cfg["max_words"]
    overlap = cfg["overlap_words"]
    min_words = cfg["min_section_words"]

    chunks: list[Chunk] = []
    for header, path, body in split_sections(doc.content):
        text = f"## {header}\n\n{body}" if header != "Document" else body
        count = len(text.split())
        if count < min_words:
            continue
        parts = [text] if count <= max_words else word_windows(text, target, overlap)
        for i, part in enumerate(parts):
            chunks.append(
                Chunk(
                    chunk_id=chunk_id(doc.tool, doc.file_path, header, i),
                    tool=doc.tool,
                    document_title=doc.title,
                    file_path=doc.file_path,
                    source_url=doc.source_url,
                    section_header=header,
                    section_path=path,
                    content=part,
                    word_count=len(part.split()),
                )
            )
    return chunks


def chunk_all(docs: list[Document]) -> list[Chunk]:
    out: list[Chunk] = []
    for doc in docs:
        out.extend(chunk_document(doc))
    return out


def save_jsonl(chunks: list[Chunk], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(chunk.model_dump_json() + "\n")


def load_chunks(path: Path) -> list[Chunk]:
    chunks: list[Chunk] = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            chunks.append(Chunk.model_validate_json(line))
    return chunks


def run_chunking() -> None:
    from src.ingest.parser import load_jsonl as load_documents

    settings = load_settings()
    docs = load_documents(root_path(settings["paths"]["processed_documents"]))
    chunks = chunk_all(docs)
    out = root_path(settings["paths"]["chunks"])
    save_jsonl(chunks, out)
    avg = sum(c.word_count for c in chunks) / max(len(chunks), 1)
    print(f"Created {len(chunks)} chunks (avg {avg:.0f} words) -> {out}")
