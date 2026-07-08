# DevOps Knowledge Copilot

**A learning project** — built to understand RAG (Retrieval-Augmented Generation) concepts through hands-on experimentation over Kubernetes and Terraform documentation.

Not a commercial product. Every script and experiment exists to learn how modern AI-assisted documentation systems work.

**Repo:** [github.com/gvarun20/devops-knowledge-copilot](https://github.com/gvarun20/devops-knowledge-copilot)  
**Website:** [gvarun20.github.io/devops-knowledge-copilot](https://gvarun20.github.io/devops-knowledge-copilot/)  
**Cost:** $0 — Python, Docker, Ollama, GitHub

---

## Start here

| I want to… | Read this |
|------------|-----------|
| **Understand the full project** (problem, plan, architecture, hurdles, scripts) | **[docs/PROJECT_DOCUMENTATION.md](docs/PROJECT_DOCUMENTATION.md)** |
| Run it for the first time | [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) |
| Follow the learning path script by script | [docs/LEARNING_PATH.md](docs/LEARNING_PATH.md) |
| Prepare for interviews | [docs/PORTFOLIO.md](docs/PORTFOLIO.md) |

---

## What this project teaches

```
Official docs → ingest → chunk → index → hybrid retrieval → LLM answer with citations
                                              ↓
                                        RAGAS evaluation + ablation
```

| Layer | What you learn |
|-------|----------------|
| **Data** | Sparse Git clone, Markdown/MDX parsing, header-aware chunking |
| **Retrieval** | Embeddings, Qdrant, BM25, RRF fusion, cross-encoder rerank |
| **Generation** | Grounded prompts, citations, refusal behavior |
| **Evaluation** | RAGAS metrics, ablation studies, honest limitations |
| **Integration** | FastAPI, static UI, Docker, CI |

---

## Quick demo

```powershell
docker compose up -d qdrant
.\scripts\dev.ps1 api          # terminal 1
python scripts/06_ask.py -i    # terminal 2 — simplest demo
```

Or browser UI: `.\scripts\dev.ps1 ui-local` → http://localhost:8080

---

## Experiments and results

| Experiment | Result | Learning |
|------------|--------|----------|
| Hybrid vs semantic-only | relevancy 0.41 → **0.89** | BM25 catches exact terms embeddings miss |
| Baseline (5 questions) | relevancy **0.70**, recall **0.47** | Retrieval is the main improvement lever |
| ~11k chunks indexed | K8s + Terraform official docs | Real-scale ingestion, not toy data |

→ [docs/EVAL_RESULTS.md](docs/EVAL_RESULTS.md)

---

## Scripts (learning order)

| # | Script | Teaches |
|---|--------|---------|
| 00 | `00_check_ollama.py` | Verify LLM is ready |
| 01 | `01_setup_data.py` | Clone doc repos |
| 02 | `02_ingest.py` | Parse documents |
| 03 | `03_chunk.py` | Header-aware chunking |
| 04 | `04_index.py` | Embeddings + Qdrant + BM25 |
| 05 | `05_query.py` | Hybrid retrieval (no LLM) |
| 06 | `06_ask.py` | Full RAG with citations |
| 07 | `07_evaluate.py` | RAGAS evaluation |
| 08 | `08_ablation.py` | Compare retrieval modes |

Full script reference → [docs/PROJECT_DOCUMENTATION.md#7-scripts-reference](docs/PROJECT_DOCUMENTATION.md#7-scripts-reference)

---

## Documentation

| Doc | Purpose |
|-----|---------|
| **[PROJECT_DOCUMENTATION.md](docs/PROJECT_DOCUMENTATION.md)** | **Master doc** — problem, plan, architecture, hurdles, scripts |
| [LEARNING_PATH.md](docs/LEARNING_PATH.md) | Week-by-week learning order |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | Technical diagrams |
| [CHUNKING.md](docs/CHUNKING.md) | Chunking design |
| [EVAL_RESULTS.md](docs/EVAL_RESULTS.md) | All experiment results |
| [PORTFOLIO.md](docs/PORTFOLIO.md) | Resume + interview guide |
| [GETTING_STARTED.md](docs/GETTING_STARTED.md) | Setup walkthrough |

---

## Stack (all free, all local)

Python · FastAPI · Qdrant · BM25 · HuggingFace embeddings · Ollama · RAGAS · Docker · GitHub Actions · GitHub Pages

---

*Built for learning. Documented for understanding. Shared for portfolio.*
