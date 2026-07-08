# Why this project exists

## The problem

DevOps and platform engineers constantly jump between **Terraform** and **Kubernetes** documentation while designing infrastructure, debugging deployments, and onboarding teammates. Official docs are authoritative but huge — thousands of pages, version-specific syntax, and search that only matches keywords.

Generic chatbots make this worse: they answer confidently from memory, often with **outdated or wrong** HCL/YAML. A wrong `lifecycle` block or a misconfigured `Deployment` spec can break production.

## Who this is for

- Engineers learning **Terraform** and **Kubernetes** in depth
- Anyone building a **portfolio-grade RAG system** with measured quality, not a demo chatbot
- A structured **learning project** with weekly milestones

## What makes this different from a tutorial clone

| Typical RAG tutorial | This project |
|---------------------|--------------|
| Fixed-size text splitting | **Header-aware chunking** aligned with doc structure |
| Vector search only | **Hybrid** semantic + BM25 + RRF + reranker |
| "It seems to work" | **RAGAS evaluation** + ablation study |
| Scraped HTML | **Official GitHub doc sources** (legal, versioned) |
| Notebook prototype | **Dockerized** pipeline + FastAPI (Week 3: deploy) |
| Paid GPT required | **Free local stack** — Ollama + local embeddings |

## Design principles

1. **Ground every answer in retrieved docs** — not the LLM's general knowledge.
2. **Say "I don't know"** when context is missing — better than hallucinating.
3. **Measure quality** — retrieval and generation scores you can show in interviews.
4. **Learn by building** — numbered scripts, small modules, documented decisions.

## Current capabilities

| Layer | Status |
|-------|--------|
| Doc ingestion (K8s + Terraform v1.9.x) | Complete |
| Header-aware chunking (~10,961 chunks) | Complete |
| Hybrid retrieval + reranking | Complete |
| LLM generation with citations (Ollama) | Complete |
| RAGAS evaluation + ablation scripts | Built — run to collect scores |
| FastAPI REST API | Built |

## Interview talking points

- Why header-aware chunking beats naive fixed-length splits
- How hybrid retrieval + reranking improved your eval numbers (ablation table)
- Why you chose local embeddings vs API embeddings (cost vs quality tradeoff)
- How you handle doc sources that moved (Terraform → `web-unified-docs`)
- How the prompt enforces faithfulness and "I don't know" behavior

## Documentation map

| Doc | Purpose |
|-----|---------|
| [GETTING_STARTED.md](GETTING_STARTED.md) | Full setup from zero |
| [WEEK1_SUMMARY.md](WEEK1_SUMMARY.md) | Retrieval pipeline achievements |
| [WEEK2_PLAN.md](WEEK2_PLAN.md) | Generation, eval, API checklist |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Diagrams and module map |
| [ROADMAP.md](ROADMAP.md) | Week 3–4 plan |
| [FREE_SETUP.md](FREE_SETUP.md) | Ollama install guide |
| [EVAL_RESULTS.md](EVAL_RESULTS.md) | Your RAGAS scores |
