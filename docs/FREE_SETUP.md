# Free/local setup — no paid API required

This project uses **Ollama** for answer generation and RAGAS evaluation.
Embeddings and reranking stay **local** (same as Week 1).

## 1. Install Ollama

Download and install: https://ollama.com

Start the Ollama app (it runs in the background on Windows).

## 2. Pull a small model

In your terminal:

```powershell
ollama pull llama3.2:3b
```

Other free options (change `model` in `config/settings.yaml`):

| Model | Size | Notes |
|-------|------|-------|
| `llama3.2:3b` | ~2 GB | Default — good balance |
| `phi3:mini` | ~2 GB | Fast on laptops |
| `mistral` | ~4 GB | Stronger, slower |

## 3. Verify Ollama is running

```powershell
ollama list
python scripts/00_check_ollama.py
```

## 4. Use the RAG pipeline

```powershell
python scripts/06_ask.py "How do I create a Kubernetes Deployment?"
```

No API key needed.

## Config

In `config/settings.yaml`:

```yaml
generation:
  provider: ollama
  model: llama3.2:3b
```

## Optional: paid OpenAI later

Set `provider: openai`, `model: gpt-4o-mini`, and add `OPENAI_API_KEY` to `.env`.

## Cost summary

| Component | Cost |
|-----------|------|
| Embeddings | Free (local) |
| Reranker | Free (local) |
| Qdrant | Free (Docker) |
| LLM answers | Free (Ollama) |
| RAGAS eval | Free (Ollama + local embeddings) |
