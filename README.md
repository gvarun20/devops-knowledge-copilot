# DevOps Knowledge Copilot

A **portfolio-grade RAG system** over official **Kubernetes** and **Terraform** documentation. It retrieves the right doc sections first, then generates **grounded answers with citations** — and says **"I don't know"** when the docs do not cover the question.

**Repository:** [github.com/gvarun20/devops-knowledge-copilot](https://github.com/gvarun20/devops-knowledge-copilot)

---

## What you get

| Capability | Description |
|------------|-------------|
| **Hybrid retrieval** | Semantic (Qdrant) + keyword (BM25) + RRF fusion + cross-encoder rerank |
| **Header-aware chunking** | Chunks follow doc structure, not arbitrary text splits |
| **Cited answers** | LLM answers only from retrieved context with source URLs |
| **Evaluation** | RAGAS metrics + ablation study across retrieval modes |
| **REST API** | FastAPI `POST /ask` and `GET /health` |
| **Zero API cost** | Local embeddings, reranker, and Ollama LLM |

**Scale (typical run):** ~1,651 documents → ~10,961 chunks → top 5 sources per question.

---

## Project status

| Week | Focus | Status |
|------|-------|--------|
| **1** | Ingest, chunk, index, hybrid retrieval | **Complete** |
| **2** | LLM generation, RAGAS eval, ablation, API | **Built** — run eval to finish |
| **3** | Chat UI, full Docker stack, public deploy | Planned |
| **4** | Monitoring, CI, portfolio polish | Planned |

---

## Prerequisites

| Tool | Purpose |
|------|---------|
| Python 3.11+ | Pipeline and API |
| Git | Clone official doc repos |
| Docker Desktop | Qdrant vector database |
| [Ollama](https://ollama.com) | Local LLM for answers and evaluation |

---

## Quick start

### 1. Clone and install

```powershell
git clone https://github.com/gvarun20/devops-knowledge-copilot.git
cd devops-knowledge-copilot

py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Start Qdrant

```powershell
docker compose up -d
```

### 3. Build the index (Week 1 — first run ~15 min)

```powershell
python scripts/01_setup_data.py
python scripts/02_ingest.py
python scripts/03_chunk.py
python scripts/04_index.py
```

### 4. Set up Ollama (Week 2 — free, no API key)

Install Ollama from [ollama.com](https://ollama.com), keep the app running, then:

```powershell
ollama pull llama3.2:3b
python scripts/00_check_ollama.py
```

Full Ollama guide → [docs/FREE_SETUP.md](docs/FREE_SETUP.md)

### 5. Ask a question

```powershell
python scripts/06_ask.py "How do I create a Kubernetes Deployment?"
python scripts/06_ask.py -i
```

**Example output:** answer with `kubectl create deployment ...` plus 5 Kubernetes doc links.

---

## How it works

```
Official docs (GitHub)
    → parse & clean
    → header-aware chunks
    → embed + index (Qdrant + BM25)
    → hybrid search + rerank
    → top 5 chunks
    → Ollama LLM (strict prompt)
    → answer + citations
```

Architecture diagrams → [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## Scripts reference

| Script | Purpose |
|--------|---------|
| `00_check_ollama.py` | Verify Ollama is running and model is pulled |
| `01_setup_data.py` | Sparse-clone K8s + Terraform doc repos |
| `02_ingest.py` | Parse Markdown/MDX → `documents.jsonl` |
| `03_chunk.py` | Header-aware chunking → `chunks.jsonl` |
| `04_index.py` | Embeddings + Qdrant + BM25 index |
| `05_query.py` | Retrieval-only test (no LLM) |
| `06_ask.py` | Full RAG: question → cited answer |
| `07_evaluate.py` | RAGAS evaluation on 38 test questions |
| `08_ablation.py` | Compare semantic / hybrid / full pipeline |

Step-by-step learning guide → [docs/LEARNING_PATH.md](docs/LEARNING_PATH.md)

---

## REST API

Start the server:

```powershell
uvicorn src.api.main:app --reload
```

Open interactive docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

**Health check:**

```powershell
curl http://127.0.0.1:8000/health
```

**Ask a question:**

```powershell
curl -X POST http://127.0.0.1:8000/ask `
  -H "Content-Type: application/json" `
  -d "{\"question\": \"What is a Terraform remote backend?\"}"
```

Response includes `answer`, `sources`, `latency_ms`, and `chunks_used`.

---

## Evaluation

Run RAGAS metrics (faithfulness, answer relevancy, context precision/recall):

```powershell
# Quick test (5 questions)
python scripts/07_evaluate.py --limit 5

# Full eval set (38 questions — slow on local LLM)
python scripts/07_evaluate.py --mode full

# Ablation: semantic vs hybrid vs full pipeline
python scripts/08_ablation.py --limit 10
```

Results are saved to `evaluation/results/`. Record scores in [docs/EVAL_RESULTS.md](docs/EVAL_RESULTS.md).

---

## Tech stack

| Layer | Technology | Notes |
|-------|------------|-------|
| Doc sources | [kubernetes/website](https://github.com/kubernetes/website), [hashicorp/web-unified-docs](https://github.com/hashicorp/web-unified-docs) | Official, versioned |
| Embeddings | `all-MiniLM-L6-v2` | Local, free |
| Vector DB | Qdrant (`qdrant/qdrant:v1.13.2`) | Docker on port 6333 |
| Keyword search | BM25 | Exact term matching |
| Fusion | Reciprocal Rank Fusion (k=60) | Merges semantic + keyword |
| Reranker | `ms-marco-MiniLM-L-6-v2` | Top 20 → top 5 |
| LLM | Ollama `llama3.2:3b` | Free/local; optional OpenAI |
| API | FastAPI + Uvicorn | `src/api/` |
| Evaluation | RAGAS | Ollama + local embeddings |

Chunking rationale → [docs/CHUNKING.md](docs/CHUNKING.md)

---

## Configuration

All tunables live in `config/settings.yaml`:

```yaml
generation:
  provider: ollama          # or openai
  model: llama3.2:3b
  base_url: http://localhost:11434/v1
```

Optional OpenAI: set `provider: openai`, add `OPENAI_API_KEY` to `.env` (see `.env.example`).

---

## Project structure

```
config/settings.yaml          # All pipeline settings
scripts/00–08_*.py            # Setup, pipeline, RAG, eval
src/
  ingest/                     # Git clone + doc parsing
  chunking/                   # Header-aware splitter
  indexing/                   # Embeddings, Qdrant, BM25
  retrieval/                  # Hybrid search + rerank
  generation/                 # Prompts + LLM client
  rag/                        # End-to-end RAG pipeline
  api/                        # FastAPI routes
  evaluation/                 # RAGAS runner
docs/                         # Project documentation
evaluation/
  questions.jsonl             # 38 hand-written eval questions
  results/                    # Saved metric JSON
data/                         # Generated locally (gitignored)
docker-compose.yml            # Qdrant service
```

Generated data (`data/raw/`, `data/processed/`, `data/chunks/`, `data/index/`) is not committed. Rebuild with scripts `01–04`.

---

## Documentation

| Document | Description |
|----------|-------------|
| [GETTING_STARTED.md](docs/GETTING_STARTED.md) | Full setup walkthrough from zero |
| [PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md) | Problem, audience, design principles |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System diagrams and module map |
| [LEARNING_PATH.md](docs/LEARNING_PATH.md) | What each script teaches |
| [WEEK1_SUMMARY.md](docs/WEEK1_SUMMARY.md) | Week 1 achievements and metrics |
| [WEEK2_PLAN.md](docs/WEEK2_PLAN.md) | Week 2 milestones and checklist |
| [FREE_SETUP.md](docs/FREE_SETUP.md) | Ollama install and model options |
| [CHUNKING.md](docs/CHUNKING.md) | Why header-aware chunking |
| [EVAL_RESULTS.md](docs/EVAL_RESULTS.md) | Template for your RAGAS scores |
| [ROADMAP.md](docs/ROADMAP.md) | Week 3–4 plan |

---

## Roadmap (brief)

| Week | Goals |
|------|-------|
| **3** | Chat UI, Docker Compose for API + Qdrant, deploy to Render/Railway, GitHub Actions CI |
| **4** | Logging/monitoring, README demo, interview prep doc, optional query rewriting |

Details → [docs/ROADMAP.md](docs/ROADMAP.md)

---

## Portfolio talking points

- **Why hybrid retrieval?** Semantic search misses exact syntax; BM25 misses paraphrases. RRF + reranking combines both.
- **Why header-aware chunking?** Keeps doc sections intact → better citations and reranker input.
- **How do you measure quality?** RAGAS faithfulness + ablation table comparing retrieval modes.
- **How is data sourced?** Official GitHub repos — legal, reproducible, version-pinned (Terraform v1.9.x).
- **Cost?** Entire stack runs free locally (embeddings, reranker, Qdrant, Ollama).

---

## Development

```powershell
pytest tests/
```

Commit from your own terminal to keep a clean GitHub contributor history:

```powershell
git add .
git commit -m "Week 2 RAG + Ollama"
git push origin main
```

---

## License

Add a [LICENSE](LICENSE) file before public portfolio use if not already present.
