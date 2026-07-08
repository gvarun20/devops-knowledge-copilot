#!/usr/bin/env python
"""DevOps Knowledge Copilot — clean light chat UI."""

from __future__ import annotations

import html
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import streamlit as st

from src.ui.api_client import api_base_url, ask_question, check_health
from src.ui.theme import inject_theme

SAMPLE_QUESTIONS = [
    ("☸️", "How do I create a Kubernetes Deployment?"),
    ("📦", "What is a Terraform remote backend?"),
    ("💓", "How do Kubernetes liveness probes work?"),
    ("🔄", "Terraform lifecycle ignore_changes"),
    ("📥", "How do I use terraform import?"),
    ("📊", "Kubernetes resource requests and limits"),
]

st.set_page_config(
    page_title="DevOps Copilot",
    page_icon="🛠️",
    layout="centered",
    initial_sidebar_state="expanded",
)


def _init_session() -> None:
    if "history" not in st.session_state:
        st.session_state.history = []


def render_hero(api_ok: bool) -> None:
    pill = "pill-live" if api_ok else "pill-off"
    status = "API online" if api_ok else "API offline"
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-icon">🛠️</div>
            <h1>DevOps Knowledge Copilot</h1>
            <p>Ask anything about Kubernetes or Terraform.
               Answers are grounded in official docs with source citations.</p>
            <div class="pill-row">
                <span class="pill {pill}">{status}</span>
                <span class="pill pill-k8s">Kubernetes</span>
                <span class="pill pill-tf">Terraform</span>
                <span class="pill pill-neutral">Hybrid RAG</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar(api_ok: bool) -> None:
    with st.sidebar:
        st.markdown("### Quick start")
        if not api_ok:
            st.error("API not running")
            st.code("uvicorn src.api.main:app --reload", language="bash")
        else:
            st.success("Ready to ask questions")

        st.markdown("---")
        st.markdown("**Example questions**")
        for icon, q in SAMPLE_QUESTIONS:
            if st.button(f"{icon}  {q[:42]}…" if len(q) > 42 else f"{icon}  {q}", key=f"sb_{q}", use_container_width=True):
                run_ask(q)
                st.rerun()

        st.markdown("---")
        st.markdown("**Stats**")
        st.metric("Documents", "~1,651")
        st.metric("Chunks", "~10,961")

        st.markdown("---")
        st.caption(f"API: `{api_base_url()}`")
        st.caption("First answer may take 1–2 min.")


def render_source_strip(source: dict) -> str:
    tool = source.get("tool", "")
    is_k8s = tool == "kubernetes"
    strip_class = "k8s" if is_k8s else "tf"
    tag_class = "k8s" if is_k8s else "tf"
    tool_label = "Kubernetes" if is_k8s else "Terraform"
    title = html.escape(source.get("document_title", ""))
    section = html.escape(source.get("section_header", ""))
    url = html.escape(source.get("source_url", ""))
    rank = source.get("rank", "?")
    return f"""
    <div class="source-strip {strip_class}">
        <span class="num">{rank}</span>
        <div class="body">
            <span class="tool-tag {tag_class}">{tool_label}</span>
            <div class="doc-title">{title}</div>
            <div class="doc-section">{section}</div>
        </div>
        <a href="{url}" target="_blank">Open ↗</a>
    </div>
    """


def render_conversation(item: dict) -> None:
    q = html.escape(item["question"])
    st.markdown(
        f"""
        <div class="bubble-user">
            <div class="label">You</div>
            <div class="text">{q}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    latency = item.get("latency_ms") or 0
    chunks = item.get("chunks_used", 0)
    st.markdown(
        f"""
        <div class="bubble-assistant">
            <div class="label">Copilot</div>
            <div class="meta">{chunks} sources · {latency / 1000:.1f}s</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(item["answer"])

    sources = item.get("sources", [])
    if sources:
        st.markdown('<div class="sources-heading">Documentation sources</div>', unsafe_allow_html=True)
        for src in sources:
            st.markdown(render_source_strip(src), unsafe_allow_html=True)


def run_ask(question: str) -> None:
    question = question.strip()
    if not question:
        st.warning("Type a question first.")
        return

    with st.spinner("Searching docs & generating answer…"):
        try:
            data = ask_question(question)
        except Exception as exc:
            st.error("Cannot reach the API. Start it in another terminal.")
            st.code("uvicorn src.api.main:app --reload", language="bash")
            st.caption(str(exc))
            return

    st.session_state.history.insert(
        0,
        {
            "question": data["question"],
            "answer": data["answer"],
            "sources": data.get("sources", []),
            "latency_ms": data.get("latency_ms"),
            "chunks_used": data.get("chunks_used", 0),
        },
    )


def main() -> None:
    inject_theme()
    _init_session()

    api_ok, _ = check_health()
    render_sidebar(api_ok)
    render_hero(api_ok)

    st.markdown('<div class="chat-card">', unsafe_allow_html=True)

    question = st.text_area(
        "Question",
        placeholder="Ask about Kubernetes or Terraform…",
        height=88,
        label_visibility="collapsed",
    )

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        ask_clicked = st.button("Get answer →", type="primary", use_container_width=True)
    with c2:
        if st.button("Clear", use_container_width=True):
            st.session_state.history = []
            st.rerun()

    if ask_clicked:
        run_ask(question)
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.history:
        for item in st.session_state.history[:5]:
            render_conversation(item)
            st.markdown("<hr style='border:none;border-top:1px solid #e2e8f0;margin:1.5rem 0;'>", unsafe_allow_html=True)
    else:
        st.markdown(
            """
            <div class="empty-state">
                <div class="icon">💬</div>
                <p>No questions yet — pick an example from the sidebar or type above.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <div class="footer-bar">
            <a href="https://github.com/gvarun20/devops-knowledge-copilot" target="_blank">GitHub</a>
            · DevOps Knowledge Copilot · answers cite official docs only
        </div>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
