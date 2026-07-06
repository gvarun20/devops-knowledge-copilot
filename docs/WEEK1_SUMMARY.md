# Week 1 — Summary & achievements

**Status: complete**

Week 1 goal: type a question → get back **5 relevant, attributed document chunks**. No LLM generation yet.

---

## What we built

```
Official docs (GitHub)
    → parse & clean
    → header-aware chunks
    → embed + index (Qdrant + BM25)
    → hybrid search + rerank
    → top 5 chunks with source URLs
```

### Pipeline scripts

| Step | Script | Output |
|------|--------|--------|
| 1 | `01_setup_data.py` | Cloned doc repos under `data/raw/` |
| 2 | `02_ingest.py` | `data/processed/documents.jsonl` |
| 3 | `03_chunk.py` | `data/chunks/chunks.jsonl` |
| 4 | `04_index.py` | Qdrant collection + `data/index/bm25_corpus.json` |
| 5 | `05_query.py` | Interactive retrieval test |

---

## Scale (your run)

| Metric | Value |
|--------|-------|
| Kubernetes documents | ~1,333 |
| Terraform documents | ~318 |
| **Total documents** | **~1,651** |
| **Total chunks** | **~10,961** |
| Average chunk size | ~167 words |

---

## Data sources

| Tool | Repository | Format |
|------|------------|--------|
| Kubernetes | [kubernetes/website](https://github.com/kubernetes/website) | Markdown — `content/en/docs/` |
| Terraform | [hashicorp/web-unified-docs](https://github.com/hashicorp/web-unified-docs) | MDX — `content/terraform/v1.9.x/docs/` |

Terraform docs moved out of the old `terraform-website` repo. We pin **v1.9.x** to avoid indexing duplicate content across every version folder.

---

## Major technical decisions

### 1. Header-aware chunking
Split on Markdown `#` headers first; only fall back to word windows for long sections (~400 words, 50 overlap).  
→ See [CHUNKING.md](CHUNKING.md)

### 2. Hybrid retrieval
- **Semantic:** Qdrant + `all-MiniLM-L6-v2` (local, no API key)
- **Keyword:** BM25 on chunk text
- **Fusion:** Reciprocal Rank Fusion (k=60)
- **Rerank:** cross-encoder `ms-marco-MiniLM-L-6-v2` — top 20 → top 5

### 3. Docker naming
Compose project: `devops-knowledge-copilot`  
Container: `devops-copilot-qdrant`

### 4. Generated data stays local
`data/raw/`, `data/processed/`, `data/chunks/`, `data/index/` are gitignored — clone and rebuild with scripts 01–04.

---

## Sample questions that work well

Use these in `05_query.py -i` to judge retrieval quality:

1. How do I create a Kubernetes Deployment?
2. What is a Terraform remote backend?
3. How do Kubernetes liveness probes work?
4. Terraform lifecycle ignore_changes
5. How do I use terraform import?
6. Kubernetes resource requests and limits
7. Terraform for_each vs count

**Good retrieval:** top results are the exact doc section you would open manually.  
**Bad retrieval:** unrelated pages rank first — tune chunking or retrieval before Week 2.

---

## What Week 1 does *not* include (by design)

- LLM-generated answers
- Evaluation metrics (RAGAS)
- REST API or web UI
- Public deployment

Those are **Week 2–3**.

---

## Known limitations

- Terraform coverage is one doc version (v1.9.x) only
- First indexing run takes ~15 minutes (model download + embedding)
- Retrieval quality depends on question phrasing — Week 2 can add query rewriting as a stretch goal
