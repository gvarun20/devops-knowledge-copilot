#!/usr/bin/env python
"""Run RAGAS evaluation (uses Ollama + local embeddings by default)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import click
from dotenv import load_dotenv

from src.evaluation.ragas_runner import run_eval

load_dotenv()


def _print_score(name: str, value: float, failures: dict) -> None:
    if value != value:  # nan
        reason = failures.get(name, "failed — try --metrics local or increase ragas_timeout")
        click.echo(f"  {name}: FAILED ({reason})")
    else:
        click.echo(f"  {name}: {value:.4f}")


@click.command()
@click.option("--mode", default="full", type=click.Choice(["full", "hybrid_no_rerank", "semantic_only"]))
@click.option("--limit", default=0, type=int, help="Max questions (0 = all)")
@click.option(
    "--metrics",
    default="local",
    type=click.Choice(["local", "full"]),
    help="local = answer_relevancy + context_recall (recommended for Ollama 3B)",
)
def main(mode: str, limit: int, metrics: str) -> None:
    click.echo(f"Metrics preset: {metrics}")
    if metrics == "full":
        click.echo("Note: full preset is slow on local Ollama (~15+ min per question).")

    result = run_eval(retrieval_mode=mode, limit=limit or None, metrics_preset=metrics)
    click.echo(f"\nMode: {result['retrieval_mode']}")
    click.echo(f"Questions: {result['num_questions']}")
    failures = result.get("failures", {})
    for name, value in result["scores"].items():
        _print_score(name, value, failures)


if __name__ == "__main__":
    main()
