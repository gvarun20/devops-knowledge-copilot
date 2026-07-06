"""Load config/settings.yaml."""

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "settings.yaml"


@lru_cache(maxsize=1)
def load_settings() -> dict[str, Any]:
    with CONFIG.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def root_path(*parts: str) -> Path:
    return ROOT.joinpath(*parts)
