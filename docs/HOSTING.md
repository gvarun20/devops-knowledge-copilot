# GitHub Pages — your live website

**URL:** https://gvarun20.github.io/devops-knowledge-copilot/

A simple portfolio site: project overview, eval metrics, example answer, link to GitHub.

---

## Enable (one time)

1. Push code to GitHub
2. Repo → **Settings** → **Pages**
3. **Build and deployment** → Source: **GitHub Actions**
4. Push to `main` — workflow `.github/workflows/pages.yml` deploys automatically

Wait 1–2 minutes, then open your URL.

---

## What's on the site

| Section | Works on GitHub Pages? |
|---------|------------------------|
| Hero + about | ✅ Always |
| Eval metrics | ✅ Always |
| Example answer | ✅ Always (static sample) |
| Live chat | ❌ Needs API on your laptop |

**Live Q&A:** clone repo → run locally → http://localhost:8080

That's normal for free RAG projects — the hosted site shows your work; interviews use screen-share demo.

---

## Update the site

Edit `docs/index.html`, then:

```powershell
git add docs/
git commit -m "Update website"
git push
```

Site updates in ~1–2 min.
