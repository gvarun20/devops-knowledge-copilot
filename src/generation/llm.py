"""LLM clients — Ollama (free/local) or OpenAI (optional)."""

from __future__ import annotations

import os
import urllib.error
import urllib.request

from openai import OpenAI

from src.config import load_settings


def generation_config() -> dict:
    return load_settings()["generation"]


def check_ollama(model: str | None = None) -> None:
    cfg = generation_config()
    base = cfg.get("ollama_host", "http://localhost:11434")
    try:
        with urllib.request.urlopen(f"{base}/api/tags", timeout=5) as resp:
            resp.read()
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(
            "Ollama is not running. Install from https://ollama.com, start the app, "
            f"then run: ollama pull {model or cfg['model']}"
        ) from exc


def openai_client() -> OpenAI:
    cfg = generation_config()
    provider = cfg.get("provider", "ollama")

    if provider == "ollama":
        check_ollama(cfg["model"])
        return OpenAI(
            base_url=cfg.get("base_url", "http://localhost:11434/v1"),
            api_key="ollama",
        )

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "generation.provider is 'openai' but OPENAI_API_KEY is not set. "
            "Switch to Ollama in config/settings.yaml or add your API key."
        )
    return OpenAI(api_key=api_key)


def ragas_llm_and_embeddings():
    """LangChain LLM + embeddings for RAGAS (all free when provider=ollama)."""
    cfg = generation_config()
    embed_name = load_settings()["embeddings"]["model_name"]

    if cfg.get("provider", "ollama") == "ollama":
        from langchain_huggingface import HuggingFaceEmbeddings
        from langchain_ollama import ChatOllama

        check_ollama(cfg["model"])
        host = cfg.get("ollama_host", "http://localhost:11434")
        timeout = load_settings().get("evaluation", {}).get("ragas_timeout", 900)
        llm = ChatOllama(
            model=cfg["model"],
            base_url=host,
            temperature=0,
            format="json",  # RAGAS faithfulness/precision need structured JSON
            num_ctx=8192,
            num_predict=2048,
            client_kwargs={"timeout": timeout},
        )
        embeddings = HuggingFaceEmbeddings(model_name=embed_name)
        return llm, embeddings

    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_openai import ChatOpenAI

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Set OPENAI_API_KEY or switch generation.provider to ollama.")
    llm = ChatOpenAI(model=cfg["model"], temperature=0)
    embeddings = HuggingFaceEmbeddings(model_name=embed_name)
    return llm, embeddings
