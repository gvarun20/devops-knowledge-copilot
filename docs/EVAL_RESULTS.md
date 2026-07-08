# Evaluation results

Run evaluations and paste scores here after each run.

## Baseline (full pipeline)

_Date:_ _not run yet_

| Metric | Score |
|--------|-------|
| faithfulness | — |
| answer_relevancy | — |
| context_precision | — |
| context_recall | — |

**Command:**
```powershell
python scripts/07_evaluate.py --mode full
```

---

## Ablation study

_Date:_ _not run yet_

| Metric | semantic_only | hybrid_no_rerank | full |
|--------|---------------|------------------|------|
| faithfulness | — | — | — |
| answer_relevancy | — | — | — |
| context_precision | — | — | — |
| context_recall | — | — | — |

**Command:**
```powershell
python scripts/08_ablation.py --limit 10
```

Raw JSON saved to `evaluation/results/`.

---

## Notes

- Evaluation uses **Ollama + local embeddings** (free; slower than cloud APIs).
- Eval set has **38 questions** in `evaluation/questions.jsonl`.
- Start with `--limit 5` on `07_evaluate.py` to test before full run.
- Update this file after each run for your portfolio README.
