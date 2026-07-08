# Project roadmap

High-level plan from retrieval prototype to portfolio-ready product.

---

## Completed

### Week 1 — Retrieval pipeline

- Sparse-clone official K8s + Terraform docs
- Parse Markdown/MDX into unified JSONL
- Header-aware chunking (~10,961 chunks)
- Local embeddings + Qdrant + BM25
- Hybrid retrieval: semantic + keyword + RRF + cross-encoder rerank
- Interactive retrieval CLI (`05_query.py`)

→ [WEEK1_SUMMARY.md](WEEK1_SUMMARY.md)

### Week 2 — Generation, evaluation, API (code complete)

- Strict prompt: answer only from context, cite sources, say "I don't know"
- Ollama integration (free/local LLM)
- Full RAG CLI (`06_ask.py`) — **tested and working**
- RAGAS evaluation runner (`07_evaluate.py`)
- Ablation study (`08_ablation.py`) — semantic vs hybrid vs full
- FastAPI (`GET /health`, `POST /ask`)
- 38-question evaluation set

**Remaining Week 2 tasks for you:**
- [ ] Run full RAGAS eval and fill [EVAL_RESULTS.md](EVAL_RESULTS.md)
- [ ] Run ablation study and document the comparison table
- [ ] Test API with curl or Swagger UI
- [ ] Push latest code to GitHub

→ [WEEK2_PLAN.md](WEEK2_PLAN.md)

---

## Week 3 — UI, deploy, CI

**Goal:** A live demo URL on your resume.

| Task | Description |
|------|-------------|
| Chat UI | Simple web frontend (Streamlit or React) calling `POST /ask` |
| Docker Compose stack | API + Qdrant in one `docker compose up` |
| Public deploy | Render, Railway, or Fly.io |
| GitHub Actions | Lint + pytest on push |
| Environment docs | Production config, secrets handling |

**Success criteria:**
- Shareable URL where anyone can ask K8s/Terraform questions
- One-command local startup for reviewers cloning the repo

---

## Week 4 — Polish and portfolio

**Goal:** Interview-ready artifact with measured quality.

| Task | Description |
|------|-------------|
| Fill eval results | Final RAGAS + ablation numbers in README or EVAL_RESULTS |
| Demo GIF / screenshot | 30-second proof in README |
| Interview prep doc | "Why hybrid?" "Why header chunking?" with your numbers |
| Logging | Request latency, retrieval mode, chunk count |
| Optional stretch | Query rewriting, Helm/Ansible docs, rate limiting on API |

**Success criteria:**
- README tells the full story in under 2 minutes of reading
- You can walk through architecture and ablation results in an interview

---

## Future ideas (post Week 4)

- Multi-version Terraform doc support
- User feedback loop (thumbs up/down on answers)
- Caching frequent questions
- OpenTelemetry tracing for retrieval latency breakdown
- Fine-tuned reranker on DevOps Q&A pairs

---

## Timeline suggestion

| When | Focus |
|------|-------|
| Now | Finish Week 2 eval + GitHub push |
| Next | Week 3 chat UI + deploy |
| After deploy | Week 4 polish + portfolio README |
