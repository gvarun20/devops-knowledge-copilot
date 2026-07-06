"""Run RAGAS evaluation on the question set."""

from __future__ import annotations

from datetime import UTC, datetime

from datasets import Dataset
from ragas import evaluate
from ragas.metrics import answer_relevancy, context_precision, context_recall, faithfulness

from src.config import load_settings, root_path
from src.evaluation.loader import load_questions, save_json
from src.generation.llm import ragas_llm_and_embeddings
from src.rag.pipeline import RAGPipeline


def run_eval(retrieval_mode: str = "full", limit: int | None = None) -> dict:
    settings = load_settings()
    questions = load_questions()
    if limit:
        questions = questions[:limit]

    pipeline = RAGPipeline(retrieval_mode=retrieval_mode)

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
    llm, embeddings = ragas_llm_and_embeddings()

    scores = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
        llm=llm,
        embeddings=embeddings,
    )

    df = scores.to_pandas()
    score_dict = {col: float(df[col].mean()) for col in df.columns if df[col].dtype.kind in "fiu"}

    result = {
        "timestamp": datetime.now(UTC).isoformat(),
        "retrieval_mode": retrieval_mode,
        "num_questions": len(questions),
        "scores": score_dict,
    }

    out_dir = root_path(settings["paths"]["eval_results"])
    stamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    save_json(out_dir / f"eval_{retrieval_mode}_{stamp}.json", result)
    return result
