from src.chunking.splitter import chunk_document
from src.config import load_settings
from src.models import Document
from src.retrieval.fusion import rrf


def test_chunking_keeps_sections():
    doc = Document(
        tool="terraform",
        title="Demo",
        file_path="demo.md",
        source_url="https://example.com",
        content="# A\n\n" + "word " * 50 + "\n# B\n\n" + "other " * 40,
    )
    chunks = chunk_document(doc)
    headers = {c.section_header for c in chunks}
    assert "A" in headers and "B" in headers


def test_rrf_boosts_overlap():
    fused = rrf([["a", "b", "c"], ["b", "a", "d"]], k=60)
    top = {x for x, _ in fused[:2]}
    assert top == {"a", "b"}


def test_env_overrides_qdrant_host(monkeypatch):
    monkeypatch.setenv("QDRANT_HOST", "my-qdrant")
    load_settings.cache_clear()
    try:
        assert load_settings()["qdrant"]["host"] == "my-qdrant"
    finally:
        load_settings.cache_clear()
        monkeypatch.delenv("QDRANT_HOST", raising=False)
