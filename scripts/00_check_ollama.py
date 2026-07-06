#!/usr/bin/env python
"""Check that Ollama is running and the configured model exists."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import json
import urllib.request

from src.config import load_settings


def main() -> None:
    cfg = load_settings()["generation"]
    host = cfg.get("ollama_host", "http://localhost:11434")
    model = cfg["model"]

    try:
        with urllib.request.urlopen(f"{host}/api/tags", timeout=5) as resp:
            data = json.loads(resp.read())
    except Exception as exc:
        print(f"Ollama not reachable at {host}")
        print("Install from https://ollama.com and start the app.")
        print(f"Then run: ollama pull {model}")
        sys.exit(1)

    names = {m.get("name", "") for m in data.get("models", [])}
    found = any(model in n or n.startswith(model) for n in names)

    print(f"Ollama OK at {host}")
    print(f"Configured model: {model}")
    if found:
        print("Model is available.")
    else:
        print(f"Model not found. Run: ollama pull {model}")
        sys.exit(1)


if __name__ == "__main__":
    main()
