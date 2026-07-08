# Evaluation results

RAGAS evaluation over the held-out question set in `evaluation/questions.jsonl` (38 questions total).

**Primary baseline:** 5 questions, full retrieval pipeline, `local` metrics preset.

Raw JSON for every run: `evaluation/results/`

---

## Environment

| Setting | Value |
|---------|-------|
| Date | 2026-07-08 |
| LLM | Ollama `llama3.2:3b` (local, free) |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` (local) |
| Reranker | `cross-encoder/ms-marco-MiniLM-L-6-v2` |
| Vector DB | Qdrant (Docker) |
| Eval framework | RAGAS 0.4.x |
| Metrics preset | `local` — see below |

### Metrics preset: `local`

Small local models struggle with RAGAS metrics that require strict JSON output (`faithfulness`, `context_precision`). The **`local`** preset measures the two metrics that run reliably on Ollama 3B:

| Metric | What it measures |
|--------|------------------|
| **answer_relevancy** | Does the generated answer address the question? |
| **context_recall** | Did retrieval return the context needed to answer? |

To attempt all four RAGAS metrics: `python scripts/07_evaluate.py --metrics full` (slower; may fail on 3B models).

---

## Baseline — full pipeline (primary result)

**Config:** `retrieval_mode=full` · **Questions:** 5 · **Preset:** local

| Metric | Score |
|--------|-------|
| answer_relevancy | **0.7012** |
| context_recall | **0.4722** |

**Command:**
```powershell
python scripts/07_evaluate.py --limit 5 --metrics local
```

**Result file:** `evaluation/results/eval_full_20260708_160739.json`

**Interpretation:** On 5 held-out questions, answers are relevant ~70% of the time. Retrieval finds roughly half of the context RAGAS expects — the main improvement lever is retrieval quality (chunking, hybrid search, reranking).

---

## Smoke test — 1 question

**Config:** `retrieval_mode=full` · **Questions:** 1 · **Preset:** local

| Metric | Score |
|--------|-------|
| answer_relevancy | **1.0000** |
| context_recall | **0.6667** |

**Result file:** `evaluation/results/eval_full_20260708_154111.json`

Single-question scores are higher than the 5-question average (expected — small sample variance).

---

## Ablation study

Compares three retrieval configurations on the **same 3 questions** using the `local` metrics preset.

| Mode | Description |
|------|-------------|
| **A — semantic_only** | Qdrant vector search only |
| **B — hybrid_no_rerank** | Semantic + BM25 + RRF fusion |
| **C — full** | Hybrid + cross-encoder rerank (top 20 → top 5) |

| Metric | semantic_only | hybrid_no_rerank | full |
|--------|---------------|------------------|------|
| answer_relevancy | 0.4099 | **0.8931** | 0.6339 |
| context_recall | 0.6796 | **0.7394** | 0.5101 |

**Command:**
```powershell
python scripts/08_ablation.py --limit 3 --metrics local
```

**Result file:** `evaluation/results/ablation_latest.json`

### Takeaways

1. **Hybrid retrieval dramatically improves answer relevancy** — semantic-only scored 41%; adding BM25 + RRF raised it to **89%** on this sample.
2. **BM25 catches what embeddings miss** — exact syntax and command names (`kubectl`, `terraform import`) rank better with keyword search.
3. **Reranker impact inconclusive at n=3** — full pipeline scored between semantic and hybrid on relevancy; context recall varied across modes. A larger eval set (10+ questions) would give a clearer reranker signal.
4. **Honest limitation:** 3 questions per mode is a small sample — treat ablation as directional, not definitive.

---

## Full metrics preset (4 RAGAS metrics) — partial runs

Attempted with `--metrics full` on Ollama 3B. Results were inconsistent due to JSON parsing failures and timeouts on `faithfulness` and `context_precision`.

| Run | Questions | answer_relevancy | context_recall | faithfulness | context_precision |
|-----|-----------|------------------|----------------|--------------|-------------------|
| Early attempt | 1 | 0.9366 | 0.4000 | timed out | timed out |

**Conclusion:** Use `--metrics local` for local Ollama evaluation, or switch to a stronger model / OpenAI for the full four-metric suite.

---

## Run history (all saved JSON)

| File | Mode | Questions | Preset | Notes |
|------|------|-----------|--------|-------|
| `eval_full_20260708_160739.json` | full | 5 | local | **Primary baseline** |
| `eval_full_20260708_154111.json` | full | 1 | local | Smoke test |
| `ablation_latest.json` | all 3 modes | 3 each | local | **Ablation study** |
| `eval_semantic_only_20260708_162745.json` | semantic_only | 3 | local | Ablation arm A |
| `eval_hybrid_no_rerank_20260708_164445.json` | hybrid_no_rerank | 3 | local | Ablation arm B |
| `eval_full_20260708_170129.json` | full | 3 | local | Ablation arm C |

---

## Portfolio talking points

- Built a **measured** RAG system — not "it seems to work" but documented RAGAS scores.
- **Hybrid retrieval** (semantic + BM25 + RRF) improved answer relevancy from **41% → 89%** vs semantic-only in ablation.
- Entire eval stack runs **free locally** (Ollama + local embeddings + Docker Qdrant).
- Acknowledged **limitations**: small eval sample, local 3B model constraints, reranker needs larger n to confirm.

---

## Commands reference

```powershell
# Primary baseline (recommended)
python scripts/07_evaluate.py --limit 5 --metrics local

# Ablation study
python scripts/08_ablation.py --limit 3 --metrics local

# Full 38-question eval (hours on local Ollama)
python scripts/07_evaluate.py --metrics local

# All 4 RAGAS metrics (may fail on 3B)
python scripts/07_evaluate.py --limit 1 --metrics full
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `No module named 'langchain_ollama'` | `pip install -r requirements.txt` |
| `Connection refused` to Qdrant | Start Docker Desktop → `docker compose up -d` |
| Scores show `nan` / `TimeoutError` | Use `--metrics local`; timeout is 900s in `config/settings.yaml` |
| `Event loop is closed` | Fixed — update to latest code; metrics run in one `evaluate()` call |
| `OutputParserException` (JSON) | Use `--metrics local`; or `format="json"` on Ollama for `--metrics full` |
| HF Hub warning | Harmless |
| `ResourceTracker` error on exit | Harmless shutdown noise — scores are still valid |

---

## Next evaluation steps

- [ ] Run baseline on **10–15 questions** for tighter confidence intervals
- [ ] Re-run ablation at **n=10** to clarify reranker impact
- [ ] Optional: `--metrics full` with `phi3:mini` or OpenAI for faithfulness / context_precision
- [ ] Link this page from README once Week 2 is pushed to GitHub
