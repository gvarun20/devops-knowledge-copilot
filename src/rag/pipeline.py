"""Full RAG pipeline: retrieve then generate."""

import time

from src.generation.answer import AnswerGenerator
from src.models import AnswerResult
from src.retrieval.pipeline import Retriever

RetrievalMode = str  # "full" | "hybrid_no_rerank" | "semantic_only"


class RAGPipeline:
    def __init__(self, retrieval_mode: str = "full") -> None:
        self.retrieval_mode = retrieval_mode
        self.retriever = Retriever(mode=retrieval_mode)
        self.generator = AnswerGenerator()

    def ask(self, question: str) -> tuple[AnswerResult, float]:
        start = time.perf_counter()
        hits = self.retriever.search(question)
        result = self.generator.generate(question, hits, mode=self.retrieval_mode)
        elapsed_ms = (time.perf_counter() - start) * 1000
        return result, elapsed_ms
