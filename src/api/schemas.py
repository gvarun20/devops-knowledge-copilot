"""FastAPI request/response models."""

from pydantic import BaseModel, Field

from src.models import SourceCitation


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=2000)


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceCitation]
    retrieval_mode: str
    chunks_used: int
    latency_ms: float


class HealthResponse(BaseModel):
    status: str = "ok"
