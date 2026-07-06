"""Shared data models."""

from pydantic import BaseModel, Field


class Document(BaseModel):
    tool: str
    title: str
    file_path: str
    source_url: str
    content: str
    word_count: int = 0


class Chunk(BaseModel):
    chunk_id: str
    tool: str
    document_title: str
    file_path: str
    source_url: str
    section_header: str
    section_path: list[str] = Field(default_factory=list)
    content: str
    word_count: int = 0


class SearchHit(BaseModel):
    chunk_id: str
    tool: str
    document_title: str
    section_header: str
    source_url: str
    content: str
    score: float
    rank: int
