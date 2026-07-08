"""HTTP client for the FastAPI backend."""

from __future__ import annotations

import os
from typing import Any

import httpx

DEFAULT_API_URL = "http://127.0.0.1:8000"
ASK_TIMEOUT = 600.0


def api_base_url() -> str:
    return os.getenv("COPILOT_API_URL", DEFAULT_API_URL).rstrip("/")


def check_health() -> tuple[bool, str]:
    try:
        with httpx.Client(timeout=5.0) as client:
            resp = client.get(f"{api_base_url()}/health")
            resp.raise_for_status()
            return True, "Connected"
    except Exception as exc:
        return False, str(exc)[:120]


def ask_question(question: str) -> dict[str, Any]:
    with httpx.Client(timeout=ASK_TIMEOUT) as client:
        resp = client.post(
            f"{api_base_url()}/ask",
            json={"question": question},
        )
        resp.raise_for_status()
        return resp.json()
