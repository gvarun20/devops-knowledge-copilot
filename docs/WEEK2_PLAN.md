# Week 2 — Plan: Generation, evaluation & API

**Week goal:** Full question → **cited answer** pipeline, wrapped in an API, with **real evaluation numbers**.

Week 1 proved retrieval. Week 2 proves the **full RAG loop** is trustworthy and measurable.

---

## Milestone checklist

By end of Week 2 you should be able to:

- [ ] Ask a question and get an **LLM answer with citations**
- [ ] See **"I don't know"** when docs don't contain the answer
- [ ] Run **RAGAS** on 30–40 test questions and record scores
- [ ] Show an **ablation table** (semantic-only vs hybrid vs full pipeline)
- [ ] Call everything via **FastAPI** (`POST /ask`, `GET /health`)

---

## Day-by-day plan

### Day 6 — Answer generation & prompt design

**Build:**
- `src/generation/prompt.py` — system prompt template
- `src/generation/answer.py` — call LLM with retrieved chunks
- `scripts/06_ask.py` — CLI: question → cited answer

**Prompt rules (non-negotiable):**
1. Answer **only** from retrieved context
2. Cite **document title + section** for each claim
3. Say **"I don't know"** if context is insufficient — do not guess

**Model choice:** API LLM you already use (OpenAI, Anthropic, etc.) — config in `config/settings.yaml` under new `generation:` section. No need to self-host.

**Done when:** 5–10 manual test questions return proper citations.

---

### Day 7 — Evaluation set

**Build:**
- `evaluation/questions.jsonl` — 30–40 hand-written Q&A pairs
- Each row: `question`, `expected_answer`, `source_tool`, `source_section`, `doc_url`

**Sources for questions:**
- 25–30 from docs you know well (cover K8s + Terraform evenly)
- 10–15 from real forum-style phrasing (Stack Overflow tags: `kubernetes`, `terraform`)

**Include hard cases:**
- Questions that **should** return "I don't know"
- Version-specific syntax questions
- Ambiguous questions (e.g. "how do I deploy?" — needs tool context)

**Done when:** diverse set that will catch failures, not just easy wins.

---

### Day 8 — RAGAS evaluation

**Build:**
- `scripts/07_evaluate.py` — run full eval set through pipeline
- `evaluation/results/` — saved JSON/CSV per run

**Metrics (RAGAS):**
| Metric | What it measures |
|--------|------------------|
| Faithfulness | Answer sticks to retrieved context (no hallucination) |
| Answer relevancy | Answer addresses the question |
| Context precision | Retrieval found the right chunks |
| Context recall | Retrieval didn't miss needed context |

**Dependencies to add:** `ragas`, `langchain-openai` (or your LLM provider adapter)

**Done when:** baseline scores documented in README / `docs/EVAL_RESULTS.md`.

---

### Day 9 — Ablation study

**Run the same eval set three times:**

| Run | Config |
|-----|--------|
| A | Semantic search only |
| B | Hybrid (semantic + BM25 + RRF), no reranker |
| C | Full pipeline (current Week 1 setup) + generation |

**Build:**
- `scripts/08_ablation.py` — runs all three, outputs comparison table
- `docs/EVAL_RESULTS.md` — table with scores per run

**This is the #1 interview artifact** — proves engineering decisions with numbers.

**Done when:** clear table showing which components help (honest if one doesn't).

---

### Day 10 — FastAPI layer

**Build:**
```
src/api/
├── main.py          # FastAPI app
├── routes.py        # /ask, /health
└── schemas.py       # request/response models
```

**Endpoints:**
| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | Liveness check |
| POST | `/ask` | `{ "question": "..." }` → answer + sources |

**Logging:** question text, latency ms, number of sources used.

**Run:** `uvicorn src.api.main:app --reload`

**Done when:** `curl` or Postman returns cited answers; Week 2 milestone complete.

---

## New files & folders (Week 2)

```
config/settings.yaml       # add generation: block
src/generation/
  prompt.py
  answer.py
src/api/
  main.py
  routes.py
  schemas.py
evaluation/
  questions.jsonl
  results/
scripts/
  06_ask.py
  07_evaluate.py
  08_ablation.py
docs/
  EVAL_RESULTS.md
```

---

## Dependencies to add (Week 2)

```
fastapi
uvicorn
ragas
langchain-openai    # or your provider
python-dotenv       # API keys in .env (never commit)
```

Add to `.env` (gitignored):
```
OPENAI_API_KEY=sk-...
```

---

## What to cut if behind schedule

| Cut first | Never cut |
|-----------|-----------|
| Ablation study (keep one eval run) | Evaluation itself |
| Extra forum-style eval questions | "I don't know" prompt behavior |
| Fancy API logging | Faithfulness / citation format |

---

## Success criteria for Week 2

1. **Demo:** one Terraform + one Kubernetes question with citations in API
2. **Numbers:** RAGAS scores written down (even if not perfect)
3. **Ablation:** table showing hybrid/reranker impact (even 3 rows)
4. **Honesty:** document where the system fails

---

## After Week 2 → Week 3 preview

- Simple chat UI
- Docker Compose for API + Qdrant
- Public deploy (Render / Railway / similar)
- CI on push

See [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for the full roadmap context.
