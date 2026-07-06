"""CLI to test retrieval (Week 1 milestone)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import click

from src.retrieval.pipeline import Retriever


@click.command()
@click.argument("question", required=False)
@click.option("-i", "--interactive", is_flag=True)
def main(question: str | None, interactive: bool) -> None:
    retriever = Retriever()

    def ask(q: str) -> None:
        click.echo(f"\nQ: {q}")
        for hit in retriever.search(q):
            preview = hit.content.replace("\n", " ")[:240]
            click.echo(f"  #{hit.rank} [{hit.tool}] {hit.document_title} — {hit.section_header}")
            click.echo(f"     {hit.source_url}")
            click.echo(f"     {preview}...")

    if interactive or not question:
        click.echo("Retrieval test (Ctrl+C to exit)")
        while True:
            q = input("> ").strip()
            if q.lower() in {"q", "quit", "exit"}:
                break
            if q:
                ask(q)
        return
    ask(question)


if __name__ == "__main__":
    main()
