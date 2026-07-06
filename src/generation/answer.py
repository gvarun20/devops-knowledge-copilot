"""LLM answer generation from retrieved chunks."""

from src.config import load_settings
from src.generation.llm import openai_client
from src.generation.prompt import build_messages
from src.models import AnswerResult, SearchHit, SourceCitation


class AnswerGenerator:
    def __init__(self) -> None:
        cfg = load_settings()["generation"]
        self.model = cfg["model"]
        self.temperature = cfg["temperature"]
        self.max_tokens = cfg["max_tokens"]
        self.client = openai_client()

    def generate(self, question: str, hits: list[SearchHit], mode: str = "full") -> AnswerResult:
        messages = build_messages(question, hits)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
        )
        answer = (response.choices[0].message.content or "").strip()

        sources = [
            SourceCitation(
                rank=h.rank,
                tool=h.tool,
                document_title=h.document_title,
                section_header=h.section_header,
                source_url=h.source_url,
            )
            for h in hits
        ]

        return AnswerResult(
            question=question,
            answer=answer,
            sources=sources,
            retrieval_mode=mode,
            chunks_used=len(hits),
        )
