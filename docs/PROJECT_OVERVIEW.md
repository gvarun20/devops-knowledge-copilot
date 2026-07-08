# Why this project exists

> **This is a learning project.** It was built to understand RAG systems through experimentation — not to deliver a product to a client.

## The problem we wanted to solve (for learning)

DevOps engineers constantly jump between **Terraform** and **Kubernetes** documentation. Official docs are authoritative but huge. Generic chatbots hallucinate version-specific syntax.

**Learning question:** Can we build a system that answers only from retrieved official docs, with citations, and measure if it actually works?

## What makes this a learning project (not a product)

| Learning project | Production product |
|-----------------|-------------------|
| Numbered scripts to understand each layer | Hidden pipeline behind one deploy button |
| Ablation experiments to compare approaches | Single "best" config chosen for users |
| Documented failures and limitations | Marketing claims |
| Free local stack (Ollama) | Paid cloud infrastructure |
| GitHub Pages portfolio site | 24/7 hosted SaaS |

## What you learn

- How document ingestion and chunking affect retrieval quality
- Why hybrid search (semantic + BM25) beats vector-only
- How to prompt an LLM to stay grounded in retrieved context
- How to evaluate RAG with RAGAS and ablation studies
- How to expose a RAG pipeline as a REST API

## Current state

| Phase | Focus | Status |
|-------|-------|--------|
| Week 1 | Retrieval pipeline | ✅ Complete |
| Week 2 | RAG + evaluation | ✅ Complete |
| Week 3 | API + UI + CI | ✅ Complete |

## Full documentation

→ **[PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)** — problem statement, planning, architecture, hurdles, scripts

## Interview talking points

- Why header-aware chunking beats fixed-size splits
- How hybrid retrieval improved eval numbers (0.41 → 0.89 relevancy)
- Why we chose local Ollama (free learning) vs OpenAI
- How we handled Terraform docs moving to MDX format
- Honest limitations: small eval set, 3B model constraints
