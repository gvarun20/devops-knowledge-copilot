# Operations guide — how teams run this project

This document follows **industry-standard** patterns: separated frontend/backend, Docker, env config, CI, and static UI on GitHub Pages.

---

## Architecture (production pattern)

```
┌─────────────────────────────────────────────────────────────────┐
│                         USERS / BROWSER                          │
└───────────────────────────────┬─────────────────────────────────┘
                                │ HTTPS
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  FRONTEND — Static UI (GitHub Pages or nginx)                    │
│  docs/index.html  ·  no Python  ·  refresh anytime             │
└───────────────────────────────┬─────────────────────────────────┘
                                │ REST JSON  POST /ask  GET /health
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│  BACKEND — FastAPI (Docker container or uvicorn)                  │
│  src/api/  ·  RAG orchestration  ·  CORS enabled                 │
└───────────────┬─────────────────────────────┬───────────────────┘
                │                             │
                ▼                             ▼
┌───────────────────────┐         ┌───────────────────────────────┐
│  Qdrant (Docker)      │         │  Ollama (host or cloud LLM)   │
│  Vector search        │         │  Answer generation            │
└───────────────────────┘         └───────────────────────────────┘
                │
                ▼
┌───────────────────────┐
│  BM25 index (file)    │
│  data/index/          │
└───────────────────────┘
```

**Rule:** UI never runs the model. API never serves HTML in production (except `/docs` for dev).

---

## Three environments

| Environment | Who uses it | How you run it |
|-------------|-------------|----------------|
| **Local dev** | You, while coding | `uvicorn` + scripts, or `docker compose up` |
| **CI** | GitHub Actions | `pytest` on every push |
| **Production** | Resume reviewers, users | GitHub Pages (UI) + Render/Railway (API, HTTPS) |

---

## Standard local workflow (recommended)

### One-time setup

```powershell
git clone https://github.com/gvarun20/devops-knowledge-copilot.git
cd devops-knowledge-copilot
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env

docker compose up -d qdrant
python scripts/01_setup_data.py
python scripts/02_ingest.py
python scripts/03_chunk.py
python scripts/04_index.py

ollama pull llama3.2:3b
```

### Daily development (backend)

```powershell
# Terminal 1 — API with hot reload
uvicorn src.api.main:app --reload

# Test
curl http://127.0.0.1:8000/health
python scripts/06_ask.py "How do I create a Kubernetes Deployment?"
```

Swagger UI: http://127.0.0.1:8000/docs

### Daily development (full stack — industry Docker Compose)

```powershell
docker compose up -d
```

| Service | URL |
|---------|-----|
| UI (nginx) | http://localhost:8080 |
| API | http://localhost:8000 |
| Qdrant | http://localhost:6333/dashboard |
| API docs | http://localhost:8000/docs |

**Requires:** index built (`04_index.py`), Ollama running on host.

Stop: `docker compose down`

---

## Configuration (12-factor)

| Source | Purpose |
|--------|---------|
| `config/settings.yaml` | Defaults, structure |
| `.env` | Secrets and local overrides (never commit) |
| Environment variables | Docker / cloud override |

| Variable | Example | Used by |
|----------|---------|---------|
| `QDRANT_HOST` | `qdrant` (in Docker) / `localhost` | API |
| `QDRANT_PORT` | `6333` | API |
| `OLLAMA_HOST` | `http://localhost:11434` | API |
| `GENERATION_PROVIDER` | `ollama` / `openai` | API |
| `OPENAI_API_KEY` | `sk-...` | API (if OpenAI) |

Docker Compose sets `QDRANT_HOST=qdrant` and `OLLAMA_HOST=http://host.docker.internal:11434` automatically.

---

## Frontend deployment (GitHub Pages)

**What pros do:** Static files on CDN/Pages — always online, no server process.

1. Push to `main` → GitHub Action deploys `docs/` to `gh-pages`
2. Enable Pages: repo **Settings → Pages → branch gh-pages**
3. URL: https://gvarun20.github.io/devops-knowledge-copilot/

**Limitation:** HTTPS Pages cannot call `http://localhost`. For public demo you need **HTTPS API** (Render/Railway).

**Local UI + local API:** use `docker compose up` (UI on :8080) or http://localhost:8080 with API on :8000.

---

## Backend deployment (next step — Render/Railway)

Industry checklist for cloud API:

1. Dockerfile (`docker/Dockerfile.api`) ✅
2. Health check `/health` ✅
3. Env vars in cloud dashboard
4. Qdrant Cloud or self-hosted Qdrant with public URL
5. Hosted LLM (OpenAI) or Ollama on GPU server
6. Paste HTTPS API URL into UI settings on GitHub Pages

---

## CI/CD (what runs on git push)

| Workflow | File | Action |
|----------|------|--------|
| **CI** | `.github/workflows/ci.yml` | `pytest` |
| **Pages** | `.github/workflows/pages.yml` | Deploy UI |

**Pro habit:** Never merge broken code — CI must pass.

```powershell
pytest tests/ -q   # run locally before push
```

---

## What NOT to do (anti-patterns)

| Anti-pattern | Industry approach |
|--------------|-------------------|
| UI calls Ollama directly | UI → API → Ollama |
| One giant Streamlit file for prod | Static/React frontend + API |
| Secrets in git | `.env` + cloud secrets |
| Manual "two terminals" in prod | Docker Compose / Kubernetes |
| No health checks | `/health` for load balancers |
| No tests in CI | GitHub Actions + pytest |

**Streamlit** (`scripts/09_ui.py`) is kept for quick experiments only — not the production UI path.

---

## Command cheat sheet

| Task | Command |
|------|---------|
| Start infra only | `docker compose up -d qdrant` |
| Full stack | `docker compose up -d` |
| API dev mode | `uvicorn src.api.main:app --reload` |
| CLI question | `python scripts/06_ask.py "..."` |
| Tests | `pytest tests/ -q` |
| Eval | `python scripts/07_evaluate.py --limit 5 --metrics local` |
| Rebuild index | `python scripts/04_index.py` |

---

## Related docs

- [HOSTING.md](HOSTING.md) — GitHub Pages details
- [ARCHITECTURE.md](ARCHITECTURE.md) — system design
- [GETTING_STARTED.md](GETTING_STARTED.md) — first-time setup
- [EVAL_RESULTS.md](EVAL_RESULTS.md) — quality metrics
