"""Run RAGAS evaluation on the question set."""

from __future__ import annotations

import math
from datetime import UTC, datetime

from src.evaluation import ragas_compat  # noqa: F401 — must load before ragas

from datasets import Dataset
from ragas import evaluate
from ragas.embeddings.base import LangchainEmbeddingsWrapper
from ragas.llms.base import LangchainLLMWrapper
from ragas.metrics import answer_relevancy, context_precision, context_recall, faithfulness
from ragas.run_config import RunConfig

from src.config import load_settings, root_path
from src.evaluation.loader import load_questions, save_json
from src.generation.llm import ragas_llm_and_embeddings
from src.rag.pipeline import RAGPipeline

METRIC_PRESETS: dict[str, list] = {
    # Reliable on llama3.2:3b — no strict JSON parsing required
    "local": [answer_relevancy, context_recall],
    # All four RAGAS metrics — needs JSON mode; slower; may fail on small models
    "full": [faithfulness, answer_relevancy, context_precision, context_recall],
}


def resolve_metrics(preset: str | None = None) -> list:
    settings = load_settings()
    name = preset or settings.get("evaluation", {}).get("metrics", "local")
    if name not in METRIC_PRESETS:
        raise ValueError(f"Unknown metrics preset '{name}'. Choose: {', '.join(METRIC_PRESETS)}")
    return METRIC_PRESETS[name]


def run_eval(
    retrieval_mode: str = "full",
    limit: int | None = None,
    metrics_preset: str | None = None,
) -> dict:
    settings = load_settings()
    questions = load_questions()
    if limit:
        questions = questions[:limit]

    pipeline = RAGPipeline(retrieval_mode=retrieval_mode)
    metrics = resolve_metrics(metrics_preset)

    rows = {
        "question": [],
        "answer": [],
        "contexts": [],
        "ground_truth": [],
    }

    for item in questions:
        hits = pipeline.retriever.search(item.question)
        result = pipeline.generator.generate(item.question, hits, mode=retrieval_mode)
        rows["question"].append(item.question)
        rows["answer"].append(result.answer)
        rows["contexts"].append([h.content for h in hits])
        rows["ground_truth"].append(item.expected_answer)

    dataset = Dataset.from_dict(rows)

    eval_cfg = settings.get("evaluation", {})
    run_config = RunConfig(
        timeout=eval_cfg.get("ragas_timeout", 900),
        max_retries=eval_cfg.get("ragas_max_retries", 1),
        max_workers=1,
    )

    llm_raw, embeddings_raw = ragas_llm_and_embeddings()
    llm = LangchainLLMWrapper(llm_raw, run_config=run_config, bypass_n=True)
    embeddings = LangchainEmbeddingsWrapper(embeddings_raw)

    preset_name = metrics_preset or settings.get("evaluation", {}).get("metrics", "local")
    failures: dict[str, str] = {}

    # Run all preset metrics in one evaluate() call — avoids "Event loop is closed"
    # when chaining multiple evaluate() calls on Windows.
    try:
        result = evaluate(
            dataset,
            metrics=metrics,
            llm=llm,
            embeddings=embeddings,
            run_config=run_config,
            batch_size=1,
            raise_exceptions=False,
        )
        df = result.to_pandas()
        score_dict: dict[str, float] = {}
        for metric in metrics:
            name = metric.name
            if name in df.columns:
                score_dict[name] = float(df[name].mean(skipna=True))
            else:
                score_dict[name] = math.nan
                failures[name] = "column missing from result"
    except Exception as exc:
        score_dict = {m.name: math.nan for m in metrics}
        failures["evaluate"] = str(exc)[:200]

    result = {
        "timestamp": datetime.now(UTC).isoformat(),
        "retrieval_mode": retrieval_mode,
        "metrics_preset": preset_name,
        "num_questions": len(questions),
        "scores": score_dict,
        "failures": failures,
    }

    out_dir = root_path(settings["paths"]["eval_results"])
    stamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    save_json(out_dir / f"eval_{retrieval_mode}_{stamp}.json", result)
    return result
