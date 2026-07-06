"""Hybrid retrieval with ablation modes."""

from __future__ import annotations

from src.chunking.splitter import load_chunks
from src.config import load_settings, root_path
from src.indexing.embedder import Embedder
from src.indexing.keyword_index import KeywordIndex
from src.indexing.vector_store import VectorStore
from src.models import Chunk, SearchHit
from src.retrieval.fusion import rrf
from src.retrieval.reranker import Reranker


def _hits_from_chunks(candidates: list[tuple[Chunk, float]], top_k: int) -> list[SearchHit]:
    hits: list[SearchHit] = []
    for rank, (chunk, score) in enumerate(candidates[:top_k], start=1):
        hits.append(
            SearchHit(
                chunk_id=chunk.chunk_id,
                tool=chunk.tool,
                document_title=chunk.document_title,
                section_header=chunk.section_header,
                source_url=chunk.source_url,
                content=chunk.content,
                score=float(score),
                rank=rank,
            )
        )
    return hits


class Retriever:
    MODES = ("full", "hybrid_no_rerank", "semantic_only")

    def __init__(self, mode: str = "full") -> None:
        if mode not in self.MODES:
            raise ValueError(f"mode must be one of {self.MODES}")
        self.mode = mode
        self.settings = load_settings()
        self.embedder = Embedder()
        self.vectors = VectorStore()
        self.keywords = KeywordIndex.load()
        self.reranker = Reranker() if mode == "full" else None
        self.by_id = {c.chunk_id: c for c in self.keywords.chunks}

    def _semantic_hits(self, question: str) -> list[tuple[Chunk, float]]:
        r_cfg = self.settings["retrieval"]
        sem = self.vectors.search(self.embedder.encode([question])[0], r_cfg["semantic_top_k"])
        out: list[tuple[Chunk, float]] = []
        for row in sem:
            chunk = self.by_id.get(row["chunk_id"])
            if chunk:
                out.append((chunk, float(row["score"])))
        return out

    def _fused_candidates(self, question: str) -> list[tuple[Chunk, float]]:
        r_cfg = self.settings["retrieval"]
        sem = self.vectors.search(self.embedder.encode([question])[0], r_cfg["semantic_top_k"])
        key = self.keywords.search(question, r_cfg["keyword_top_k"])
        fused = rrf(
            [[h["chunk_id"] for h in sem], [c.chunk_id for c, _ in key]],
            k=r_cfg["rrf_k"],
        )
        k_cfg = self.settings["reranker"]
        candidates: list[tuple[Chunk, float]] = []
        for cid, score in fused[: k_cfg["top_k_fusion"]]:
            chunk = self.by_id.get(cid)
            if chunk:
                candidates.append((chunk, score))
        return candidates

    def search(self, question: str) -> list[SearchHit]:
        k_final = self.settings["reranker"]["top_k_final"]

        if self.mode == "semantic_only":
            return _hits_from_chunks(self._semantic_hits(question), k_final)

        if self.mode == "hybrid_no_rerank":
            return _hits_from_chunks(self._fused_candidates(question), k_final)

        candidates = self._fused_candidates(question)
        assert self.reranker is not None
        return self.reranker.rerank(question, candidates, k_final)


def run_indexing() -> None:
    from tqdm import tqdm

    from src.chunking.splitter import load_chunks, save_jsonl

    settings = load_settings()
    chunks_path = root_path(settings["paths"]["chunks"])
    chunks = load_chunks(chunks_path)

    embedder = Embedder()
    store = VectorStore()
    store.reset(embedder.dim)

    texts = [c.content for c in chunks]
    vectors: list[list[float]] = []
    bs = settings["embeddings"]["batch_size"]
    for i in tqdm(range(0, len(texts), bs), desc="Embedding"):
        vectors.extend(embedder.encode(texts[i : i + bs]))

    store.upsert(chunks, vectors)
    path = KeywordIndex(chunks).save()
    print(f"Indexed {len(chunks)} chunks in Qdrant + {path}")
