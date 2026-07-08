# Getting started — full walkthrough

This guide takes you from a fresh clone to a working **question → cited answer** system.

**Time:** ~30 minutes first run (indexing dominates; ~15 min for step 4 alone).

---

## What you are building

1. **Index** official Kubernetes and Terraform docs locally
2. **Retrieve** the best 5 doc sections for any question
3. **Generate** an answer with citations using a free local LLM (Ollama)

---

## Step 0 — Prerequisites

Install and verify:

| Tool | Check |
|------|-------|
| Python 3.11+ | `py -3 --version` |
| Git | `git --version` |
| Docker Desktop | `docker --version` |
| Ollama | [ollama.com](https://ollama.com) — needed for Week 2 |

---

## Step 1 — Project setup

```powershell
git clone https://github.com/gvarun20/devops-knowledge-copilot.git
cd devops-knowledge-copilot

py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## Step 2 — Start Qdrant

Qdrant stores vector embeddings for semantic search.

```powershell
docker compose up -d
docker ps
```

You should see `devops-copilot-qdrant` on port **6333**.

Dashboard (optional): [http://localhost:6333/dashboard](http://localhost:6333/dashboard)

---

## Step 3 — Build the document index

Run these **in order**. Each script prints progress.

### 3a. Clone doc repos (sparse checkout)

```powershell
python scripts/01_setup_data.py
```

Clones:
- [kubernetes/website](https://github.com/kubernetes/website) — Markdown under `content/en/docs/`
- [hashicorp/web-unified-docs](https://github.com/hashicorp/web-unified-docs) — Terraform v1.9.x MDX

Output: `data/raw/`

### 3b. Parse documents

```powershell
python scripts/02_ingest.py
```

Output: `data/processed/documents.jsonl` (~1,651 documents)

### 3c. Chunk documents

```powershell
python scripts/03_chunk.py
```

Output: `data/chunks/chunks.jsonl` (~10,961 chunks)

Uses **header-aware chunking** — see [CHUNKING.md](CHUNKING.md).

### 3d. Embed and index

```powershell
python scripts/04_index.py
```

This step:
- Downloads embedding and reranker models (first run only)
- Upserts vectors into Qdrant
- Builds BM25 keyword index

Output: Qdrant collection `devops_docs` + `data/index/bm25_corpus.json`

**Expect ~15 minutes** on first run.

---

## Step 4 — Test retrieval (no LLM)

Verify search works before adding generation:

```powershell
python scripts/05_query.py "How do I create a Kubernetes Deployment?"
python scripts/05_query.py -i
```

**Good sign:** top results are the exact Kubernetes doc pages you would open manually.

---

## Step 5 — Set up Ollama (free LLM)

### Install and start

1. Download from [ollama.com](https://ollama.com)
2. Keep the Ollama app running (system tray on Windows)

### Pull the model

```powershell
ollama pull llama3.2:3b
```

~2 GB download.

### Verify

```powershell
ollama list
python scripts/00_check_ollama.py
```

More model options → [FREE_SETUP.md](FREE_SETUP.md)

---

## Step 6 — Full RAG (question → answer)

```powershell
python scripts/06_ask.py "How do I create a Kubernetes Deployment?"
```

You should see:
- A grounded answer (often with `kubectl` examples)
- **Sources** — ranked list with doc title, section, and URL

Interactive mode (faster after first question — models stay loaded):

```powershell
python scripts/06_ask.py -i
```

Type `quit` to exit.

**Note:** First answer can take 1–2 minutes on a laptop. This is normal for a local 3B model.

---

## Step 7 — REST API (optional)

```powershell
uvicorn src.api.main:app --reload
```

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Health: `GET /health`
- Ask: `POST /ask` with body `{"question": "..."}`

---

## Step 8 — Evaluation (optional)

Measure quality with RAGAS:

```powershell
# Quick smoke test
python scripts/07_evaluate.py --limit 5

# Full run (38 questions — slow)
python scripts/07_evaluate.py

# Ablation study
python scripts/08_ablation.py --limit 10
```

Record scores in [EVAL_RESULTS.md](EVAL_RESULTS.md).

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `Connection refused` to Qdrant | `docker compose up -d` |
| `Ollama is not running` | Start Ollama app; run `ollama pull llama3.2:3b` |
| `Model not found` | `ollama pull llama3.2:3b` |
| Empty or bad retrieval | Re-run `04_index.py`; check Qdrant is up |
| Slow answers | Use `-i` mode; close heavy apps; first run is always slowest |
| HF Hub warning | Harmless; set `HF_TOKEN` only for faster model downloads |
| `ResourceTracker` error on exit | Harmless shutdown noise from a dependency; answer still valid |

---

## Rebuild from scratch

If you delete `data/` or Qdrant volume:

```powershell
docker compose down -v   # wipes Qdrant data
docker compose up -d
python scripts/01_setup_data.py
python scripts/02_ingest.py
python scripts/03_chunk.py
python scripts/04_index.py
```

Doc repos in `data/raw/` can be reused — skip `01` if still present.

---

## Next steps

- [LEARNING_PATH.md](LEARNING_PATH.md) — what each script teaches
- [ARCHITECTURE.md](ARCHITECTURE.md) — system design
- [ROADMAP.md](ROADMAP.md) — Week 3 UI and deployment
