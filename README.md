# DevOps Knowledge Copilot

**Portfolio project** — RAG over official Kubernetes & Terraform docs. Grounded answers with citations.

**Cost: $0** — Python, Docker (Qdrant only), Ollama, GitHub. No cloud, no API keys.

**Repo:** [github.com/gvarun20/devops-knowledge-copilot](https://github.com/gvarun20/devops-knowledge-copilot)

**Live site:** [gvarun20.github.io/devops-knowledge-copilot](https://gvarun20.github.io/devops-knowledge-copilot/)

---

## For recruiters (30-second summary)

Built a **hybrid RAG pipeline** (Qdrant + BM25 + reranker) over ~11k doc chunks. Measured with **RAGAS**: answer relevancy **0.70**, hybrid retrieval beats vector-only **0.41 → 0.89**. Exposed via **FastAPI** + static UI. All local, no paid services.

Full interview script → **[docs/PORTFOLIO.md](docs/PORTFOLIO.md)**

---

## Demo in an interview (2 terminals)

**Before the call:** index built once, Ollama running, `ollama pull llama3.2:3b`

```powershell
# Terminal 1 — start services + API
.\scripts\dev.ps1 demo

# Terminal 2 — chat UI in browser
.\scripts\dev.ps1 ui-local
```

Open **http://localhost:8080** → ask: *"How do I create a Kubernetes Deployment?"*

**Even simpler (no browser):** `python scripts/06_ask.py -i`

---

## First-time setup (one time, ~30 min)

```powershell
git clone https://github.com/gvarun20/devops-knowledge-copilot.git
cd devops-knowledge-copilot
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

docker compose up -d qdrant
python scripts/01_setup_data.py
python scripts/02_ingest.py
python scripts/03_chunk.py
python scripts/04_index.py
ollama pull llama3.2:3b
```

Details → [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)

---

## What you built (resume bullets)

- Hybrid retrieval (semantic + BM25 + RRF + cross-encoder rerank) over official K8s/Terraform docs
- RAG pipeline with citation-backed answers via local LLM (Ollama)
- RAGAS evaluation + ablation study with published metrics
- FastAPI REST API (`/ask`, `/health`) + static chat UI
- CI with pytest on every push

---

## Eval results

| Metric | Score |
|--------|-------|
| answer_relevancy | 0.70 |
| context_recall | 0.47 |
| hybrid vs semantic-only (relevancy) | 0.41 → **0.89** |

→ [docs/EVAL_RESULTS.md](docs/EVAL_RESULTS.md)

---

## Commands

```powershell
.\scripts\dev.ps1 demo      # Start Qdrant + print demo steps
.\scripts\dev.ps1 api       # API (terminal 1)
.\scripts\dev.ps1 ui-local  # UI (terminal 2)
.\scripts\dev.ps1 ask       # CLI chat
.\scripts\dev.ps1 test      # pytest
```

---

## Stack (all free)

| Piece | Tool |
|-------|------|
| Vector DB | Qdrant (Docker) |
| Keyword search | BM25 (local file) |
| Embeddings | HuggingFace (local) |
| LLM | Ollama `llama3.2:3b` |
| API | FastAPI |
| UI | Static HTML (`docs/index.html`) |
| Hosting | GitHub repo + **GitHub Pages** website |

---

## GitHub Pages website

**https://gvarun20.github.io/devops-knowledge-copilot/**

Portfolio site with overview, metrics, and example answer. Enable: **Settings → Pages → GitHub Actions**.

Live chat: run locally with `.\scripts\dev.ps1 ui-local`. Details → [docs/HOSTING.md](docs/HOSTING.md)

---

## Docs

| Doc | When to read |
|-----|--------------|
| **[PORTFOLIO.md](docs/PORTFOLIO.md)** | **Before interviews** |
| [HOSTING.md](docs/HOSTING.md) | Enable GitHub Pages |
| [GETTING_STARTED.md](docs/GETTING_STARTED.md) | First setup |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design questions |
| [EVAL_RESULTS.md](docs/EVAL_RESULTS.md) | Metrics deep-dive |
