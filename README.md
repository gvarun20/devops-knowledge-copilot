# DevOps Knowledge Copilot

Personal **learning project**: build a RAG system that answers questions from official **Kubernetes** and **Terraform** documentation — with citations, not guesswork.

This repo is structured for step-by-step learning. Read `docs/LEARNING_PATH.md` for the Week 1 flow.

## What Week 1 does

```
Docs → parse → chunk → embed → hybrid search → rerank → top 5 chunks
```

No LLM generation yet. Week 1 proves **retrieval** works.

## Setup

**Requirements:** Python 3.11+, Git, Docker Desktop

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
docker compose up -d
```

## Run the pipeline

```powershell
python scripts/01_setup_data.py
python scripts/02_ingest.py
python scripts/03_chunk.py
python scripts/04_index.py      # first run ~15 min
python scripts/05_query.py "How do I create a Kubernetes Deployment?"
python scripts/05_query.py -i
```

## Project layout

```
config/settings.yaml     # paths, models, chunk sizes
scripts/01–05_*.py       # run in order
src/
  ingest/                # clone + parse docs
  chunking/              # header-aware splitter
  indexing/              # embeddings, Qdrant, BM25
  retrieval/             # hybrid + RRF + reranker
docs/                    # learning notes
data/                    # generated locally (not in git)
```

## Tech stack

| Piece | Choice |
|-------|--------|
| Embeddings | `all-MiniLM-L6-v2` (local, free) |
| Vector DB | Qdrant (Docker) |
| Keyword | BM25 |
| Fusion | Reciprocal Rank Fusion |
| Reranker | `ms-marco-MiniLM-L-6-v2` |

## Git

You manage version control from your own VS Code terminal:

```powershell
git init
git add .
git commit -m "Week 1 RAG pipeline"
git remote add origin https://github.com/gvarun20/devops-knowledge-copilot.git
git push -u origin main
```

Keep commit messages **short** (under 30 characters).

## Roadmap

- **Week 2:** LLM answers + citations, evaluation (RAGAS)
- **Week 3:** API, UI, deploy
- **Week 4:** Docs polish, monitoring
