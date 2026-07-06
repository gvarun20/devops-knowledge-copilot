#!/usr/bin/env python
"""Ablation study: compare retrieval modes with RAGAS."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import click
from dotenv import load_dotenv

from src.evaluation.loader import save_json
from src.evaluation.ragas_runner import run_eval
from src.config import root_path, load_settings

load_dotenv()

MODES = [
    ("semantic_only", "A — semantic only"),
    ("hybrid_no_rerank", "B — hybrid, no rerank"),
    ("full", "C — full pipeline"),
]


@click.command()
@click.option("--limit", default=10, type=int, help="Questions per mode (keep low to save API cost)")
def main(limit: int) -> None:
    table: dict[str, dict] = {}
    for mode, label in MODES:
        click.echo(f"\nRunning {label} ...")
        table[mode] = run_eval(retrieval_mode=mode, limit=limit)

    click.echo("\n=== Ablation summary ===")
    header = f"{'Metric':<22}" + "".join(f"{m:<18}" for m, _ in MODES)
    click.echo(header)

    metrics = set()
    for row in table.values():
        metrics.update(row["scores"].keys())

    for metric in sorted(metrics):
        line = f"{metric:<22}"
        for mode, _ in MODES:
            val = table[mode]["scores"].get(metric, float("nan"))
            line += f"{val:<18.4f}"
        click.echo(line)

    out = root_path(load_settings()["paths"]["eval_results"]) / "ablation_latest.json"
    save_json(out, {"modes": table})
    click.echo(f"\nSaved {out}")


if __name__ == "__main__":
    main()
