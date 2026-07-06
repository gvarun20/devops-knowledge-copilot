# Learning path — Week 1

Run scripts in order. Each step teaches one part of a RAG retrieval pipeline.

| Step | Script | What you learn |
|------|--------|----------------|
| 1 | `01_setup_data.py` | Clone official doc repos (sparse checkout) |
| 2 | `02_ingest.py` | Parse Markdown/MDX into a unified format |
| 3 | `03_chunk.py` | Header-aware chunking |
| 4 | `04_index.py` | Embeddings + Qdrant + BM25 |
| 5 | `05_query.py` | Hybrid search + reranking |

**Milestone:** ask a question → get 5 ranked doc chunks with sources. No LLM yet (Week 2).

## Concepts to read about

- Embeddings and cosine similarity
- BM25 keyword search
- Reciprocal Rank Fusion
- Cross-encoder reranking
- Vector databases (Qdrant)

See `docs/CHUNKING.md` for the chunking design note.
