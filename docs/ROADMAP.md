# Project roadmap

## Completed

### Week 1 — Retrieval pipeline ✅
Sparse clone, chunk, index, hybrid search + rerank.

### Week 2 — RAG + evaluation + API ✅
Ollama generation, RAGAS eval, ablation, FastAPI `/ask`.

### Week 3 — Industry-standard ops ✅
- **Docker Compose:** Qdrant + API + nginx UI (`docker compose up`)
- **Dockerfile** for API (`docker/Dockerfile.api`)
- **Static UI** on GitHub Pages (`docs/index.html`)
- **CI:** pytest on push (`.github/workflows/ci.yml`)
- **12-factor config:** env vars override YAML
- **Operations guide:** [OPERATIONS.md](OPERATIONS.md)
- **Dev script:** `scripts/dev.ps1`

---

## Week 4 — Cloud production (next)

| Task | Industry practice |
|------|-------------------|
| Deploy API to **Render** or **Railway** | HTTPS backend, health checks |
| Point GitHub Pages UI to cloud API URL | Full public demo |
| Optional: **Qdrant Cloud** | Managed vector DB |
| Optional: **OpenAI** for 24/7 LLM | No dependency on laptop Ollama |
| README demo GIF | Portfolio polish |

**Success:** One HTTPS UI link + one HTTPS API link on resume.

---

## Optional later

- GitHub Actions: build & push Docker image
- Staging environment
- Prometheus metrics on `/health` + latency
- Next.js frontend (if targeting frontend roles)
