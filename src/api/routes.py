"""API routes."""

import logging
import time

from fastapi import APIRouter, HTTPException

from src.api.schemas import AskRequest, AskResponse, HealthResponse
from src.rag.pipeline import RAGPipeline

logger = logging.getLogger("devops-copilot")
router = APIRouter()
_pipeline: RAGPipeline | None = None


def get_pipeline() -> RAGPipeline:
    global _pipeline
    if _pipeline is None:
        _pipeline = RAGPipeline(retrieval_mode="full")
    return _pipeline


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()


@router.post("/ask", response_model=AskResponse)
def ask(body: AskRequest) -> AskResponse:
    question = body.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    start = time.perf_counter()
    try:
        result, _ = get_pipeline().ask(question)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    latency_ms = (time.perf_counter() - start) * 1000

    logger.info("ask q=%r chunks=%d ms=%.0f", question[:80], result.chunks_used, latency_ms)

    return AskResponse(
        question=result.question,
        answer=result.answer,
        sources=result.sources,
        retrieval_mode=result.retrieval_mode,
        chunks_used=result.chunks_used,
        latency_ms=round(latency_ms, 1),
    )
