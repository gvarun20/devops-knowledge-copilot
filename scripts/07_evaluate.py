#!/usr/bin/env python
"""Run RAGAS evaluation (uses Ollama + local embeddings by default)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import click
from dotenv import load_dotenv

from src.evaluation.ragas_runner import run_eval

load_dotenv()


@click.command()
@click.option("--mode", default="full", type=click.Choice(["full", "hybrid_no_rerank", "semantic_only"]))
@click.option("--limit", default=0, type=int, help="Max questions (0 = all)")
def main(mode: str, limit: int) -> None:
    result = run_eval(retrieval_mode=mode, limit=limit or None)
    click.echo(f"Mode: {result['retrieval_mode']}")
    click.echo(f"Questions: {result['num_questions']}")
    for name, value in result["scores"].items():
        click.echo(f"  {name}: {value:.4f}")


if __name__ == "__main__":
    main()
