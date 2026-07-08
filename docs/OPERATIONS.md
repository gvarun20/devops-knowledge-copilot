# How to run the demo

Simple guide for a **free local portfolio project**. No cloud, no paid services.

---

## Architecture (what to explain in interviews)

```
UI (browser)  →  FastAPI  →  Qdrant + BM25  →  Ollama
```

The UI never runs the model. The API does all RAG work.

---

## One-time setup

See [GETTING_STARTED.md](GETTING_STARTED.md) — clone, venv, build index, pull Ollama model.

---

## Every demo / interview

**Checklist:**
1. Ollama app running (system tray)
2. Qdrant running: `docker compose up -d qdrant`
3. API running: `.\scripts\dev.ps1 api`
4. (Optional) UI: `.\scripts\dev.ps1 ui-local` → http://localhost:8080

Or skip the UI: `python scripts/06_ask.py -i`

---

## Commands

| Task | Command |
|------|---------|
| Start Qdrant | `docker compose up -d qdrant` |
| Demo helper | `.\scripts\dev.ps1 demo` |
| API | `.\scripts\dev.ps1 api` |
| Browser UI | `.\scripts\dev.ps1 ui-local` |
| CLI chat | `python scripts/06_ask.py -i` |
| Tests | `pytest tests/ -q` |
| Eval | `python scripts/07_evaluate.py --limit 5 --metrics local` |
| Stop Qdrant | `docker compose down` |

---

## Full Docker stack (optional)

If you want to show Docker skills:

```powershell
docker compose up -d --build
```

UI :8080, API :8000. Still needs Ollama on your host. **Not required** for interviews — Qdrant-only Docker + local Python is simpler.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| API offline | Start `.\scripts\dev.ps1 api` |
| Qdrant error | `docker compose up -d qdrant` |
| Ollama error | Open Ollama app; `ollama pull llama3.2:3b` |
| Slow first answer | Normal (~1–2 min); use `-i` mode after first question |
| GitHub Pages can't answer | Expected — demo locally instead |

---

## Related

- [PORTFOLIO.md](PORTFOLIO.md) — resume + interview script
- [ARCHITECTURE.md](ARCHITECTURE.md) — design details
