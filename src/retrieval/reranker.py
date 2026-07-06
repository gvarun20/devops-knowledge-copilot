"""Cross-encoder reranker."""

from sentence_transformers import CrossEncoder

from src.config import load_settings
from src.models import Chunk, SearchHit


class Reranker:
    def __init__(self) -> None:
        name = load_settings()["reranker"]["model_name"]
        self.model = CrossEncoder(name)

    def rerank(self, query: str, items: list[tuple[Chunk, float]], top_k: int) -> list[SearchHit]:
        if not items:
            return []
        pairs = [(query, c.content) for c, _ in items]
        scores = self.model.predict(pairs)
        ranked = sorted(zip(items, scores, strict=True), key=lambda x: float(x[1]), reverse=True)[:top_k]
        hits: list[SearchHit] = []
        for rank, ((chunk, _), score) in enumerate(ranked, start=1):
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
