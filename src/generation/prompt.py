"""Prompt templates for grounded answer generation."""

from src.config import load_settings
from src.models import SearchHit

SYSTEM_PROMPT = """You are a DevOps documentation assistant for Terraform and Kubernetes.

Rules:
1. Answer ONLY using the provided documentation excerpts.
2. Cite sources inline as [Source N] matching the excerpt numbers.
3. If the excerpts do not contain enough information, respond with exactly:
   "{unknown_phrase}"
4. Do not use general knowledge. Do not guess syntax or flags.
5. Keep answers concise and practical."""


def build_messages(question: str, hits: list[SearchHit]) -> list[dict[str, str]]:
    cfg = load_settings()["generation"]
    unknown = cfg["unknown_phrase"]

    if not hits:
        return [
            {"role": "system", "content": SYSTEM_PROMPT.format(unknown_phrase=unknown)},
            {"role": "user", "content": f"Question: {question}\n\nNo documentation excerpts were retrieved."},
        ]

    blocks: list[str] = []
    for hit in hits:
        blocks.append(
            f"[Source {hit.rank}] ({hit.tool}) {hit.document_title} — {hit.section_header}\n"
            f"URL: {hit.source_url}\n"
            f"{hit.content}"
        )

    context = "\n\n---\n\n".join(blocks)
    user = f"Question: {question}\n\nDocumentation excerpts:\n\n{context}"

    return [
        {"role": "system", "content": SYSTEM_PROMPT.format(unknown_phrase=unknown)},
        {"role": "user", "content": user},
    ]
