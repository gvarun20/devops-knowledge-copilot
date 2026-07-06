"""Load and save evaluation datasets."""

import json
from pathlib import Path

from src.config import load_settings, root_path
from src.models import EvalQuestion


def load_questions(path: Path | None = None) -> list[EvalQuestion]:
    src = path or root_path(load_settings()["paths"]["eval_questions"])
    items: list[EvalQuestion] = []
    with src.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(EvalQuestion.model_validate_json(line))
    return items


def save_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
