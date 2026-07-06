"""Tests for Week 2 generation prompt."""

from src.generation.prompt import build_messages
from src.models import SearchHit


def test_prompt_includes_unknown_instruction():
    hits = [
        SearchHit(
            chunk_id="abc",
            tool="kubernetes",
            document_title="Deployments",
            section_header="Create",
            source_url="https://kubernetes.io/docs/",
            content="Use kubectl create deployment.",
            score=0.9,
            rank=1,
        )
    ]
    messages = build_messages("How do I create a Deployment?", hits)
    assert "Answer ONLY" in messages[0]["content"]
    assert "[Source 1]" in messages[1]["content"]
    assert "Deployments" in messages[1]["content"]
