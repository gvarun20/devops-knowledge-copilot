#!/usr/bin/env python
"""Ask a question — retrieval + cited LLM answer."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import click
from dotenv import load_dotenv

from src.rag.pipeline import RAGPipeline

load_dotenv()


def print_answer(result, latency_ms: float) -> None:
    click.echo(f"\nAnswer ({latency_ms:.0f} ms):\n")
    click.echo(result.answer)
    click.echo("\nSources:")
    for s in result.sources:
        click.echo(f"  [{s.rank}] [{s.tool}] {s.document_title} — {s.section_header}")
        click.echo(f"      {s.source_url}")


@click.command()
@click.argument("question", required=False)
@click.option("-i", "--interactive", is_flag=True)
@click.option("--mode", default="full", type=click.Choice(["full", "hybrid_no_rerank", "semantic_only"]))
def main(question: str | None, interactive: bool, mode: str) -> None:
    pipeline = RAGPipeline(retrieval_mode=mode)

    def run(q: str) -> None:
        try:
            result, ms = pipeline.ask(q)
        except RuntimeError as exc:
            click.echo(f"Error: {exc}", err=True)
            return
        print_answer(result, ms)

    if interactive or not question:
        click.echo("DevOps Copilot — full RAG (Ctrl+C to exit)")
        while True:
            q = input("> ").strip()
            if q.lower() in {"q", "quit", "exit"}:
                break
            if q:
                run(q)
        return
    run(question)


if __name__ == "__main__":
    main()
