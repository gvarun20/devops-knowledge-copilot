# DevOps Knowledge Copilot

A **learning project** that builds a production-style RAG system over official **Kubernetes** and **Terraform** documentation — grounded answers with citations, not guesswork.

**Repository:** [github.com/gvarun20/devops-knowledge-copilot](https://github.com/gvarun20/devops-knowledge-copilot)

---

## Why this project?

DevOps docs are huge and version-specific. Generic chatbots hallucinate syntax. This system retrieves the **exact doc sections** first, then generates answers only from that context — and says **"I don't know"** when the docs don't cover it.

Full rationale → [docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md)

---

## Current status

| Week | Focus | Status |
|------|-------|--------|
| **1** | Retrieval pipeline | **Done** |
| **2** | LLM answers + RAGAS eval + API | **In progress** |
| **3** | UI + deploy + CI | Upcoming |
| **4** | Monitoring + portfolio polish | Upcoming |

### Week 1 at a glance

~**1,651** documents → ~**10,961** chunks → hybrid search → **top 5 cited chunks**

Details → [docs/WEEK1_SUMMARY.md](docs/WEEK1_SUMMARY.md)

---

## Quick start

**Requirements:** Python 3.11+, Git, Docker Desktop

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
docker compose up -d
```

**Run pipeline (in order):**

```powershell
python scripts/01_setup_data.py
python scripts/02_ingest.py
python scripts/03_chunk.py
python scripts/04_index.py      # ~15 min first run
python scripts/05_query.py -i   # interactive retrieval test
```

### Week 2 — generation & API (free / local)

Uses **Ollama** — no paid GPT required. Full guide → [docs/FREE_SETUP.md](docs/FREE_SETUP.md)

```powershell
# 1. Install Ollama from https://ollama.com
ollama pull llama3.2:3b

pip install -r requirements.txt
python scripts/00_check_ollama.py
python scripts/06_ask.py "How do I create a Kubernetes Deployment?"
python scripts/06_ask.py -i
python scripts/07_evaluate.py --limit 5
python scripts/08_ablation.py --limit 5
uvicorn src.api.main:app --reload
```

API: `POST http://127.0.0.1:8000/ask` with body `{"question": "..."}`

---

## How it works

```
Docs → parse → chunk → embed → hybrid search → rerank → top 5 chunks
                                              ↓ (Week 2)
                                    LLM answer + citations
```

Architecture diagram → [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## Tech stack

| Layer | Technology | Why |
|-------|------------|-----|
| Embeddings | `all-MiniLM-L6-v2` | Free, local, reproducible |
| Vector DB | Qdrant (Docker) | Real vector store, hybrid-ready |
| Keyword | BM25 | Catches exact terms embeddings miss |
| Fusion | Reciprocal Rank Fusion | Simple, proven merge |
| Reranker | `ms-marco-MiniLM-L-6-v2` | Reorders top 20 → top 5 |
| LLM (Week 2) | **Ollama** `llama3.2:3b` (free, local) | No API key; optional OpenAI in config |

Chunking design → [docs/CHUNKING.md](docs/CHUNKING.md)

---

## Project structure

```
config/settings.yaml       # all tunables
scripts/01–08_*.py         # pipeline + Week 2 tools
src/
  ingest/                  # clone + parse docs
  chunking/                # header-aware splitter
  indexing/                # embeddings, Qdrant, BM25
  retrieval/               # hybrid + RRF + reranker
  generation/              # LLM prompts + answers
  rag/                     # retrieve + generate
  api/                     # FastAPI
  evaluation/              # RAGAS runner
docs/                      # project documentation
evaluation/
  questions.jsonl          # eval dataset
  results/                 # saved metrics
data/                      # generated locally (gitignored)
docker-compose.yml         # Qdrant
```

---

## Documentation

| Doc | Contents |
|-----|----------|
| [PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md) | Why we built this, design principles |
| [WEEK1_SUMMARY.md](docs/WEEK1_SUMMARY.md) | Achievements, metrics, decisions |
| [WEEK2_PLAN.md](docs/WEEK2_PLAN.md) | Day-by-day Week 2 build plan |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System diagrams + module map |
| [LEARNING_PATH.md](docs/LEARNING_PATH.md) | Week 1 script guide |
| [FREE_SETUP.md](docs/FREE_SETUP.md) | Free Ollama setup (no paid API) |
| [CHUNKING.md](docs/CHUNKING.md) | Chunking rationale |
| [EVAL_RESULTS.md](docs/EVAL_RESULTS.md) | Template for your scores |

---

## Git workflow

Commit from **your VS Code terminal** (keeps you as sole contributor):

```powershell
git add .
git commit -m "Week 1 RAG pipeline"   # keep under 30 chars
git push
```

---

## What makes this portfolio-worthy

- Measured retrieval quality (Week 2 RAGAS + ablation)
- Hybrid search — not naive vector-only RAG
- Legally clean data from official GitHub doc repos
- Dockerized, reproducible pipeline
- Documented engineering decisions you can explain in interviews

---

## License

See [LICENSE](LICENSE) if present, or add one before public portfolio use.
