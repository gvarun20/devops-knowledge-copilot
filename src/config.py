"""Load config/settings.yaml with environment overrides."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "settings.yaml"


def _apply_env(settings: dict[str, Any]) -> dict[str, Any]:
    """Override YAML from environment variables (12-factor app pattern)."""
    qdrant = settings.setdefault("qdrant", {})
    if host := os.getenv("QDRANT_HOST"):
        qdrant["host"] = host
    if port := os.getenv("QDRANT_PORT"):
        qdrant["port"] = int(port)

    gen = settings.setdefault("generation", {})
    if ollama := os.getenv("OLLAMA_HOST"):
        ollama = ollama.rstrip("/")
        gen["ollama_host"] = ollama
        gen["base_url"] = f"{ollama}/v1"
    if provider := os.getenv("GENERATION_PROVIDER"):
        gen["provider"] = provider
    if model := os.getenv("GENERATION_MODEL"):
        gen["model"] = model

    return settings


@lru_cache(maxsize=1)
def load_settings() -> dict[str, Any]:
    with CONFIG.open(encoding="utf-8") as f:
        return _apply_env(yaml.safe_load(f))


def root_path(*parts: str) -> Path:
    return ROOT.joinpath(*parts)
