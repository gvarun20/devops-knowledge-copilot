"""BM25 keyword index."""

from __future__ import annotations

import json
import re
from pathlib import Path

from rank_bm25 import BM25Okapi

from src.config import load_settings, root_path
from src.models import Chunk

TOKEN = re.compile(r"[a-z0-9]+")


class KeywordIndex:
    def __init__(self, chunks: list[Chunk]) -> None:
        self.chunks = chunks
        self.tokens = [TOKEN.findall(c.content.lower()) for c in chunks]
        self.index = BM25Okapi(self.tokens)

    def search(self, query: str, top_k: int) -> list[tuple[Chunk, float]]:
        q = TOKEN.findall(query.lower())
        if not q:
            return []
        scores = self.index.get_scores(q)
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)[:top_k]
        return [(self.chunks[i], float(s)) for i, s in ranked if s > 0]

    def save(self, path: Path | None = None) -> Path:
        out = path or root_path(load_settings()["paths"]["bm25_corpus"])
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps([c.model_dump() for c in self.chunks]), encoding="utf-8")
        return out

    @classmethod
    def load(cls, path: Path | None = None) -> KeywordIndex:
        src = path or root_path(load_settings()["paths"]["bm25_corpus"])
        chunks = [Chunk.model_validate(x) for x in json.loads(src.read_text(encoding="utf-8"))]
        return cls(chunks)
