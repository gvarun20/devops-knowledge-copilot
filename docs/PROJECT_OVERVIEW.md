# Why this project exists

## The problem

DevOps and platform engineers constantly jump between **Terraform** and **Kubernetes** documentation while designing infrastructure, debugging deployments, and onboarding teammates. Official docs are authoritative but huge — thousands of pages, version-specific syntax, and search that only matches keywords.

Generic chatbots make this worse: they answer confidently from memory, often with **outdated or wrong** HCL/YAML. A wrong `lifecycle` block or a misconfigured `Deployment` spec can break production.

## Who this is for

- Engineers learning **Terraform** and **Kubernetes** in depth
- Anyone building a **portfolio-grade RAG system** with measured quality, not a demo chatbot
- You — as a structured **learning project** with weekly milestones

## What makes this different from a tutorial clone

| Typical RAG tutorial | This project |
|---------------------|--------------|
| Fixed-size text splitting | **Header-aware chunking** aligned with doc structure |
| Vector search only | **Hybrid** semantic + BM25 + RRF + reranker |
| "It seems to work" | **RAGAS evaluation** + ablation study (Week 2) |
| Scraped HTML | **Official GitHub doc sources** (legal, versioned) |
| Notebook prototype | **Dockerized** pipeline you can deploy (Week 3) |

## Design principles

1. **Ground every answer in retrieved docs** — not the LLM's general knowledge (Week 2).
2. **Say "I don't know"** when context is missing — better than hallucinating.
3. **Measure quality** — retrieval and generation scores you can show in interviews.
4. **Learn by building** — numbered scripts, small modules, documented decisions.

## Interview talking points (after Week 2)

- Why header-aware chunking beats naive fixed-length splits
- How hybrid retrieval + reranking improved your eval numbers (ablation table)
- Why you chose local embeddings vs API embeddings (cost vs quality tradeoff)
- How you handle doc sources that moved (Terraform → `web-unified-docs`)

See [WEEK1_SUMMARY.md](WEEK1_SUMMARY.md) for what is already built and [WEEK2_PLAN.md](WEEK2_PLAN.md) for what comes next.
