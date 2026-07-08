# Hosting the UI on GitHub Pages

> **Start with [OPERATIONS.md](OPERATIONS.md)** for the full industry workflow (local Docker, CI, env config).

The **UI** is static HTML on GitHub Pages. The **API** runs separately (Docker or cloud).

---

## Live URL (after deploy)

**https://gvarun20.github.io/devops-knowledge-copilot/**

(Push to `main` → GitHub Action deploys `docs/` to `gh-pages` branch.)

---

## Important: UI ≠ API

| Part | Hosted where | Always on? |
|------|----------------|------------|
| **UI** (`docs/index.html`) | GitHub Pages | Yes — just refresh browser |
| **API** | Your PC or Render/Railway | Only when you start it |

The webpage calls your API over HTTP. **Refresh the browser** anytime — no need to restart Streamlit.

---

## HTTPS vs localhost (read this)

GitHub Pages is **HTTPS**. Browsers **block** HTTPS pages from calling `http://127.0.0.1:8000`.

So from the **live GitHub URL**:

- You **cannot** use localhost API (security restriction)
- You **need** a public **HTTPS** API (Week 3 deploy to Render/Railway)

### Workaround for local dev (same PC)

Run the UI from your machine (HTTP, not GitHub):

```powershell
cd E:\SUMMER_PROJECT_2ND
uvicorn src.api.main:app --reload
```

Second terminal:

```powershell
python -m http.server 8080 --directory docs
```

Open **http://localhost:8080** → set API URL to `http://127.0.0.1:8000` → works.

---

## Enable GitHub Pages (one time)

1. GitHub repo → **Settings** → **Pages**
2. Source: **Deploy from branch**
3. Branch: **gh-pages** / **root**
4. Save

Or push `docs/` — the workflow creates `gh-pages` automatically.

---

## Deploy steps

```powershell
git add docs/ .github/workflows/pages.yml src/api/main.py
git commit -m "Add GitHub Pages UI"
git push origin main
```

Wait ~1–2 min → open your Pages URL.

---

## API URL in the UI

The page saves **API base URL** in your browser (localStorage).

- Local: `http://127.0.0.1:8000`
- After cloud deploy: `https://your-app.onrender.com`

Status pill shows **API online** / **API offline** and rechecks every 15 seconds.

---

## Stop using Streamlit (optional)

You can use GitHub Pages UI instead of Streamlit:

- **Always available** UI (static HTML)
- **Refresh browser** to reload — no Python UI process
- Still start **API + Docker + Ollama** when you want answers

Streamlit (`scripts/09_ui.py`) remains optional for local dev.
