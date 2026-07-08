# DevOps Knowledge Copilot

RAG system over official **Kubernetes** and **Terraform** documentation — grounded answers with citations.

**Repository:** [github.com/gvarun20/devops-knowledge-copilot](https://github.com/gvarun20/devops-knowledge-copilot)

---

## How it is built (industry pattern)

```
Frontend (static UI)  →  Backend (FastAPI)  →  Qdrant + BM25 + LLM
   GitHub Pages            Docker / uvicorn       Ollama (local)
```

| Layer | Technology | Role |
|-------|------------|------|
| **Frontend** | `docs/index.html` on GitHub Pages | User interface — refresh anytime |
| **Backend** | FastAPI `POST /ask` | RAG logic — never in the browser |
| **Data** | Qdrant + BM25 files | Hybrid retrieval |
| **LLM** | Ollama (local) or OpenAI | Answer generation |

Full operations guide → **[docs/OPERATIONS.md](docs/OPERATIONS.md)** (read this to learn the pro workflow)

---

## Quick start (standard workflow)

### 1. Install

```powershell
git clone https://github.com/gvarun20/devops-knowledge-copilot.git
cd devops-knowledge-copilot
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

### 2. Build index (one time, ~15 min)

```powershell
docker compose up -d qdrant
python scripts/01_setup_data.py
python scripts/02_ingest.py
python scripts/03_chunk.py
python scripts/04_index.py
ollama pull llama3.2:3b
```

### 3. Run full stack (one command — recommended)

```powershell
docker compose up -d --build
```

| Service | URL |
|---------|-----|
| **UI** | http://localhost:8080 |
| **API** | http://localhost:8000/docs |
| **Health** | http://localhost:8000/health |

Keep **Ollama** running on your machine.

### 4. Or: API dev mode (hot reload)

```powershell
.\scripts\dev.ps1 api
```

---

## Dev commands (`scripts/dev.ps1`)

```powershell
.\scripts\dev.ps1 up        # Docker: Qdrant + API + UI
.\scripts\dev.ps1 down      # Stop containers
.\scripts\dev.ps1 api       # Local API with reload
.\scripts\dev.ps1 test      # pytest (same as CI)
.\scripts\dev.ps1 ask       # CLI chat
.\scripts\dev.ps1 help      # All commands
```

---

## Public UI (GitHub Pages)

**https://gvarun20.github.io/devops-knowledge-copilot/**

Deploys automatically on push to `main`. For answers, point the UI to a running **HTTPS API** (local API works with `docker compose up` + http://localhost:8080).

---

## CI (runs on every push)

- **Tests:** `pytest` via [.github/workflows/ci.yml](.github/workflows/ci.yml)
- **UI deploy:** GitHub Pages via [.github/workflows/pages.yml](.github/workflows/pages.yml)

Run locally before push: `pytest tests/ -q`

---

## Evaluation results

| Metric | Score (5 questions) |
|--------|---------------------|
| answer_relevancy | 0.70 |
| context_recall | 0.47 |

Ablation: hybrid retrieval **0.41 → 0.89** answer relevancy vs semantic-only.

Details → [docs/EVAL_RESULTS.md](docs/EVAL_RESULTS.md)

---

## Project structure

```
docker/Dockerfile.api       # API container (production pattern)
docker-compose.yml          # Qdrant + API + nginx UI
src/api/                    # FastAPI backend
src/rag/                    # RAG pipeline
docs/index.html             # Static frontend (GitHub Pages)
scripts/01–08_*.py          # Data pipeline + eval
scripts/dev.ps1             # Standard dev commands
config/settings.yaml        # Defaults (+ env overrides)
.github/workflows/          # CI + Pages
```

Streamlit (`scripts/09_ui.py`) is **optional** — for experiments only, not production.

---

## Documentation

| Doc | Purpose |
|-----|---------|
| **[OPERATIONS.md](docs/OPERATIONS.md)** | **How teams run this (start here)** |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design |
| [HOSTING.md](docs/HOSTING.md) | GitHub Pages |
| [GETTING_STARTED.md](docs/GETTING_STARTED.md) | First-time walkthrough |
| [EVAL_RESULTS.md](docs/EVAL_RESULTS.md) | RAGAS scores |
| [ROADMAP.md](docs/ROADMAP.md) | Deploy API to cloud (next) |

---

## Status

| Week | Focus | Status |
|------|-------|--------|
| 1 | Retrieval pipeline | Done |
| 2 | RAG + eval + API | Done |
| 3 | Docker stack + UI + CI | Done |
| 4 | Cloud API deploy (Render) | Next |

---

## License

Add [LICENSE](LICENSE) before public portfolio use if not present.
