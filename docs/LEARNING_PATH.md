# Learning path

> **This is a learning project.** Run scripts in order — each step teaches one layer of a RAG system before the next depends on it.

**Full project documentation:** [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)

---

## Week 1 — Retrieval

| Step | Script | What you learn |
|------|--------|----------------|
| 0 | — | Install Python, Docker, create venv |
| 1 | `01_setup_data.py` | Sparse Git checkout of large doc repos |
| 2 | `02_ingest.py` | Parse Markdown/MDX into a unified document format |
| 3 | `03_chunk.py` | Header-aware chunking (not fixed-size splits) |
| 4 | `04_index.py` | Sentence embeddings, Qdrant upsert, BM25 build |
| 5 | `05_query.py` | Hybrid search, RRF fusion, cross-encoder rerank |

**Week 1 milestone:** ask a question → get 5 ranked doc chunks with source URLs. No LLM yet.

Summary → [WEEK1_SUMMARY.md](WEEK1_SUMMARY.md)

---

## Week 2 — Generation and evaluation

| Step | Script | What you learn |
|------|--------|----------------|
| 0 | `00_check_ollama.py` | Verify local LLM is ready |
| 6 | `06_ask.py` | Full RAG: retrieve → prompt → cited answer |
| 7 | `07_evaluate.py` | RAGAS metrics on a fixed question set |
| 8 | `08_ablation.py` | Compare retrieval modes with numbers |
| — | `uvicorn src.api.main:app` | Expose RAG as a REST API |

**Week 2 milestone:** grounded answers with citations, measurable eval scores, API endpoint.

Plan → [WEEK2_PLAN.md](WEEK2_PLAN.md)  
Ollama setup → [FREE_SETUP.md](FREE_SETUP.md)

---

## Concepts to understand

### Retrieval
- **Embeddings** — text → vectors; cosine similarity for semantic search
- **BM25** — keyword scoring; catches exact terms embeddings miss
- **Reciprocal Rank Fusion** — merge two ranked lists without score normalization
- **Cross-encoder reranking** — score query–passage pairs jointly for better top-k

### Generation
- **Grounded generation** — LLM constrained to retrieved context only
- **Citation format** — tie each claim to a doc title + section + URL
- **Refusal behavior** — "I don't know" when context is insufficient

### Evaluation
- **Faithfulness** — answer sticks to retrieved chunks (no hallucination)
- **Answer relevancy** — answer addresses the question
- **Context precision** — retrieved chunks are relevant
- **Context recall** — retrieval found everything needed to answer

---

## Sample questions to try

Use these in `05_query.py -i` (retrieval) or `06_ask.py -i` (full RAG):

1. How do I create a Kubernetes Deployment?
2. What is a Terraform remote backend?
3. How do Kubernetes liveness probes work?
4. Terraform lifecycle ignore_changes
5. How do I use terraform import?
6. Kubernetes resource requests and limits
7. Terraform for_each vs count

---

## Key files to read in the codebase

| Topic | File |
|-------|------|
| Chunking logic | `src/chunking/splitter.py` |
| Hybrid retrieval | `src/retrieval/pipeline.py` |
| RRF fusion | `src/retrieval/fusion.py` |
| System prompt | `src/generation/prompt.py` |
| End-to-end RAG | `src/rag/pipeline.py` |
| All settings | `config/settings.yaml` |

Chunking design → [CHUNKING.md](CHUNKING.md)  
Architecture → [ARCHITECTURE.md](ARCHITECTURE.md)

---

## What's next

Project is **complete for portfolio use**. Optional polish → [ROADMAP.md](ROADMAP.md)
