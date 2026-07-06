# Architecture

## End-to-end flow (Week 1)

```mermaid
flowchart TB
    subgraph sources [Data sources]
        K8s[kubernetes/website]
        TF[web-unified-docs]
    end

    subgraph pipeline [Local pipeline]
        Clone[01 setup_data]
        Parse[02 ingest]
        Chunk[03 chunk]
        Index[04 index]
        Query[05 query]
    end

    subgraph storage [Storage]
        JSONL[(documents.jsonl / chunks.jsonl)]
        Qdrant[(Qdrant vector DB)]
        BM25[(BM25 corpus JSON)]
    end

    subgraph retrieval [Retrieval layer]
        Sem[Semantic search]
        Key[BM25 search]
        RRF[Reciprocal Rank Fusion]
        Rerank[Cross-encoder rerank]
    end

    K8s --> Clone
    TF --> Clone
    Clone --> Parse --> Chunk --> Index
    Parse --> JSONL
    Chunk --> JSONL
    Index --> Qdrant
    Index --> BM25
    Query --> Sem
    Query --> Key
    Sem --> RRF
    Key --> RRF
    RRF --> Rerank
    Qdrant --> Sem
    BM25 --> Key
    Rerank --> Results[Top 5 chunks + URLs]
```

## Week 2 addition (planned)

```mermaid
flowchart LR
    Q[User question] --> Ret[Week 1 retrieval]
    Ret --> Ctx[Top 5 chunks]
    Ctx --> LLM[LLM + strict prompt]
    LLM --> Ans[Answer + citations]
    LLM --> IDK[I don't know if no context]
```

## Module map

```
src/
├── config.py              # settings.yaml loader
├── models.py              # Document, Chunk, SearchHit
├── ingest/
│   ├── setup.py           # git sparse clone
│   └── parser.py          # Markdown/MDX → JSONL
├── chunking/
│   └── splitter.py        # header-aware chunks
├── indexing/
│   ├── embedder.py        # sentence-transformers
│   ├── vector_store.py    # Qdrant client
│   └── keyword_index.py   # BM25
└── retrieval/
    ├── fusion.py          # RRF
    ├── reranker.py        # cross-encoder
    └── pipeline.py        # Retriever + run_indexing
```

## Configuration

All tunables live in `config/settings.yaml`:

| Section | Controls |
|---------|----------|
| `paths` | File locations for data |
| `doc_sources` | Git repos, globs, URL bases |
| `chunking` | Word targets, overlap |
| `embeddings` | Model name, batch size |
| `reranker` | Model, top-k before/after rerank |
| `qdrant` | Host, port, collection name |
| `retrieval` | Semantic/keyword top-k, RRF k |

## Infrastructure (local)

| Service | Image | Port |
|---------|-------|------|
| Qdrant | `qdrant/qdrant:v1.13.2` | 6333 |

Start: `docker compose up -d`
