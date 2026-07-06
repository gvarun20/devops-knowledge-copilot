"""Hybrid retrieval: semantic + BM25 + RRF + rerank."""

from src.chunking.splitter import load_chunks
from src.config import load_settings, root_path
from src.indexing.embedder import Embedder
from src.indexing.keyword_index import KeywordIndex
from src.indexing.vector_store import VectorStore
from src.models import Chunk, SearchHit
from src.retrieval.fusion import rrf
from src.retrieval.reranker import Reranker


class Retriever:
    def __init__(self) -> None:
        self.settings = load_settings()
        self.embedder = Embedder()
        self.vectors = VectorStore()
        self.keywords = KeywordIndex.load()
        self.reranker = Reranker()
        self.by_id = {c.chunk_id: c for c in self.keywords.chunks}

    def search(self, question: str) -> list[SearchHit]:
        cfg = self.settings
        r_cfg = cfg["retrieval"]
        k_cfg = cfg["reranker"]

        sem = self.vectors.search(self.embedder.encode([question])[0], r_cfg["semantic_top_k"])
        key = self.keywords.search(question, r_cfg["keyword_top_k"])

        fused = rrf(
            [[h["chunk_id"] for h in sem], [c.chunk_id for c, _ in key]],
            k=r_cfg["rrf_k"],
        )[: k_cfg["top_k_fusion"]]

        candidates: list[tuple[Chunk, float]] = []
        for cid, score in fused:
            chunk = self.by_id.get(cid)
            if chunk:
                candidates.append((chunk, score))

        return self.reranker.rerank(question, candidates, k_cfg["top_k_final"])


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
