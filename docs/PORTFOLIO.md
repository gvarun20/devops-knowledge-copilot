# Portfolio guide — get the job

This is a **demo project for your resume**, not a product for clients. Keep it **simple and free**.

---

## What to put on your resume

**Project title:** DevOps Knowledge Copilot — RAG over Kubernetes & Terraform docs

**One line:**
> Built a hybrid RAG system (Qdrant + BM25 + reranker) with RAGAS evaluation; FastAPI backend; $0 local stack.

**Bullet points (pick 3–4):**
- Ingested ~1,650 official K8s/Terraform docs into ~11k chunks with header-aware splitting
- Implemented hybrid retrieval (semantic + BM25 + RRF + cross-encoder rerank)
- Measured quality with RAGAS: answer relevancy 0.70; ablation showed hybrid beat vector-only (0.41 → 0.89)
- Exposed pipeline via FastAPI; static UI; pytest CI on GitHub Actions

**Link:** GitHub repo URL only. You do **not** need a live public URL.

---

## How to demo in an interview (5 minutes)

### Before the call (10 min setup)

1. Open Ollama (system tray — must be running)
2. Start Qdrant: `docker compose up -d qdrant`
3. Quick test: `python scripts/06_ask.py "What is a Kubernetes Deployment?"`

If that works, you are ready.

### During the call — Option A: Browser (looks best)

**Terminal 1:**
```powershell
.\scripts\dev.ps1 api
```

**Terminal 2:**
```powershell
.\scripts\dev.ps1 ui-local
```

Share screen → **http://localhost:8080** → ask a sample question → show answer + **source citations**.

### During the call — Option B: Terminal (simplest)

```powershell
python scripts/06_ask.py -i
```

No UI, no extra terminal. Still shows RAG + citations.

---

## What to say (talk track)

1. **Problem:** DevOps docs are huge; engineers need fast, accurate answers with sources.
2. **Approach:** RAG over official docs only — no hallucinated URLs.
3. **Retrieval:** Hybrid search beats vector-only (show ablation numbers).
4. **Eval:** RAGAS metrics, not gut feel.
5. **Stack:** Python, FastAPI, Qdrant, Ollama — all free, runs on my laptop.

---

## Questions interviewers ask

| Question | Your answer |
|----------|-------------|
| Why hybrid retrieval? | Vector misses exact terms (`kubectl`, `for_each`); BM25 misses paraphrases. RRF merges both. Ablation: relevancy 0.41 → 0.89. |
| How do you reduce hallucinations? | Strict prompt: answer only from retrieved chunks; cite sources; say "I don't know" if missing. |
| How did you measure quality? | RAGAS on 38 questions; published scores in EVAL_RESULTS.md. |
| Why Ollama not OpenAI? | Free, local, good for portfolio; same architecture works with OpenAI via config. |
| Why not Streamlit for prod? | Separated UI + API is standard; static HTML + REST is simpler to explain and deploy. |

---

## GitHub Pages website

Put this URL on your resume alongside the repo:

**https://gvarun20.github.io/devops-knowledge-copilot/**

The site shows what you built (architecture, metrics, example answer). Interviewers can browse it without cloning.

Live Q&A still runs on your laptop during screen-share — that's fine and free.

Enable: repo **Settings → Pages → Source: GitHub Actions** → push to `main`.

---

## Checklist before applying

- [ ] Repo is public on GitHub
- [ ] README has eval numbers and architecture
- [ ] You can run demo in under 5 minutes
- [ ] You can explain hybrid retrieval without reading notes
- [ ] `pytest tests/ -q` passes

**You are done.** No Render, no Railway, no credit card.
