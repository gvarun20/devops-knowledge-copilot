# Week 2 — Generation, evaluation & API

**Week goal:** Full question → **cited answer** pipeline, wrapped in an API, with **real evaluation numbers**.

Week 1 proved retrieval. Week 2 proves the **full RAG loop** is trustworthy and measurable.

---

## Milestone checklist

| Task | Status |
|------|--------|
| Ask a question and get an **LLM answer with citations** | **Done** — `06_ask.py` tested |
| See **"I don't know"** when docs don't contain the answer | **Built** — prompt enforces this |
| Run **RAGAS** on 38 test questions and record scores | **Built** — run `07_evaluate.py` |
| Show an **ablation table** (semantic vs hybrid vs full) | **Built** — run `08_ablation.py` |
| Call everything via **FastAPI** (`POST /ask`, `GET /health`) | **Built** — run `uvicorn` |

---

## What was built

### Generation layer
- `src/generation/prompt.py` — system prompt template
- `src/generation/answer.py` — call LLM with retrieved chunks
- `src/generation/llm.py` — Ollama (default) or optional OpenAI
- `scripts/06_ask.py` — CLI: question → cited answer

**Prompt rules:**
1. Answer **only** from retrieved context
2. Cite **document title + section** for each claim
3. Say **"I don't know"** if context is insufficient — do not guess

### Evaluation
- `evaluation/questions.jsonl` — 38 hand-written Q&A pairs
- `scripts/07_evaluate.py` — RAGAS on full pipeline
- `scripts/08_ablation.py` — compare three retrieval modes
- `docs/EVAL_RESULTS.md` — template for your scores

**RAGAS metrics:**

| Metric | What it measures |
|--------|------------------|
| Faithfulness | Answer sticks to retrieved context |
| Answer relevancy | Answer addresses the question |
| Context precision | Retrieval found the right chunks |
| Context recall | Retrieval didn't miss needed context |

### API
- `src/api/main.py`, `routes.py`, `schemas.py`
- `GET /health` — liveness
- `POST /ask` — `{ "question": "..." }` → answer + sources + latency

Run: `uvicorn src.api.main:app --reload`

### Free LLM setup
- Default: **Ollama** `llama3.2:3b` — no API key
- `scripts/00_check_ollama.py` — verify install
- Guide: [FREE_SETUP.md](FREE_SETUP.md)

---

## Your remaining tasks

### 1. Run evaluation (start small)

```powershell
python scripts/07_evaluate.py --limit 5
python scripts/07_evaluate.py --mode full
```

Paste scores into [EVAL_RESULTS.md](EVAL_RESULTS.md).

### 2. Run ablation study

```powershell
python scripts/08_ablation.py --limit 10
```

This is the **#1 interview artifact** — proves which components help.

### 3. Test the API

```powershell
uvicorn src.api.main:app --reload
```

Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### 4. Push to GitHub

```powershell
git add .
git commit -m "Week 2 RAG + Ollama"
git push origin main
```

---

## Ablation modes

| Run | Config | CLI mode |
|-----|--------|----------|
| A | Semantic search only | `semantic_only` |
| B | Hybrid (semantic + BM25 + RRF), no reranker | `hybrid_no_rerank` |
| C | Full pipeline + generation | `full` |

---

## Success criteria for Week 2

1. **Demo:** one Terraform + one Kubernetes question with citations (CLI or API)
2. **Numbers:** RAGAS scores written in EVAL_RESULTS.md
3. **Ablation:** table showing hybrid/reranker impact
4. **Honesty:** document where the system fails

---

## What to cut if behind schedule

| Cut first | Never cut |
|-----------|-----------|
| Full 38-question eval (use `--limit 10`) | At least one eval run with scores |
| Ablation (keep one mode comparison) | "I don't know" prompt behavior |
| Fancy API logging | Faithfulness / citation format |

---

## After Week 2

→ [ROADMAP.md](ROADMAP.md) — Week 3 UI, deploy, CI
