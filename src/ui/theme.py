"""Modern light theme for the Streamlit UI."""

from __future__ import annotations

import streamlit as st

# Light doc-assistant palette (distinct from OpenFlights dark dashboard)
BG = "#f4f6f9"
SURFACE = "#ffffff"
BORDER = "#e2e8f0"
TEXT = "#1e293b"
MUTED = "#64748b"
ACCENT = "#0d9488"
ACCENT_LIGHT = "#ccfbf1"
K8S = "#2563eb"
K8S_LIGHT = "#dbeafe"
TF = "#9333ea"
TF_LIGHT = "#f3e8ff"
USER_BUBBLE = "#ecfdf5"
USER_BORDER = "#99f6e4"
WARN = "#f59e0b"
GREEN = "#16a34a"


def inject_theme() -> None:
    st.markdown(
        f"""
        <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,600;0,9..40,700;1,9..40,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
        <style>
        .stApp {{
            background: linear-gradient(180deg, {BG} 0%, #eef2f7 100%);
            font-family: "DM Sans", -apple-system, sans-serif;
        }}
        header[data-testid="stHeader"] {{ background: transparent; }}
        .block-container {{
            max-width: 960px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }}
        /* Hide default streamlit chrome for cleaner look */
        #MainMenu, footer {{ visibility: hidden; }}

        .hero {{
            text-align: center;
            padding: 2rem 1rem 1.5rem;
            margin-bottom: 1.5rem;
        }}
        .hero-icon {{
            width: 56px; height: 56px;
            background: linear-gradient(135deg, {ACCENT} 0%, #0891b2 100%);
            border-radius: 16px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 1.6rem;
            margin-bottom: 0.75rem;
            box-shadow: 0 8px 24px rgba(13, 148, 136, 0.25);
        }}
        .hero h1 {{
            font-size: 1.85rem;
            font-weight: 700;
            color: {TEXT};
            margin: 0 0 0.35rem;
            letter-spacing: -0.02em;
        }}
        .hero p {{
            color: {MUTED};
            font-size: 1rem;
            margin: 0 auto;
            max-width: 520px;
            line-height: 1.5;
        }}
        .pill-row {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 0.45rem;
            margin-top: 1rem;
        }}
        .pill {{
            font-size: 0.72rem;
            font-weight: 600;
            padding: 0.3rem 0.75rem;
            border-radius: 999px;
            letter-spacing: 0.02em;
        }}
        .pill-live {{ background: #dcfce7; color: {GREEN}; }}
        .pill-off {{ background: #fee2e2; color: #dc2626; }}
        .pill-k8s {{ background: {K8S_LIGHT}; color: {K8S}; }}
        .pill-tf {{ background: {TF_LIGHT}; color: {TF}; }}
        .pill-neutral {{ background: {SURFACE}; color: {MUTED}; border: 1px solid {BORDER}; }}

        .chat-card {{
            background: {SURFACE};
            border: 1px solid {BORDER};
            border-radius: 20px;
            padding: 1.5rem;
            box-shadow: 0 4px 24px rgba(15, 23, 42, 0.06);
            margin-bottom: 1.25rem;
        }}

        .bubble-user {{
            background: {USER_BUBBLE};
            border: 1px solid {USER_BORDER};
            border-radius: 16px 16px 4px 16px;
            padding: 1rem 1.15rem;
            margin-bottom: 1rem;
        }}
        .bubble-user .label {{
            font-size: 0.68rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: {ACCENT};
            margin-bottom: 0.35rem;
        }}
        .bubble-user .text {{
            color: {TEXT};
            font-size: 0.95rem;
            line-height: 1.55;
        }}

        .bubble-assistant {{
            background: {SURFACE};
            border: 1px solid {BORDER};
            border-radius: 4px 16px 16px 16px;
            padding: 1.15rem 1.25rem;
            margin-bottom: 1rem;
        }}
        .bubble-assistant .label {{
            font-size: 0.68rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.06em;
            color: {MUTED};
            margin-bottom: 0.5rem;
        }}
        .bubble-assistant .meta {{
            font-size: 0.75rem;
            color: {MUTED};
            margin-bottom: 0.75rem;
            font-family: "JetBrains Mono", monospace;
        }}
        .bubble-assistant .text {{
            color: {TEXT};
            font-size: 0.92rem;
            line-height: 1.65;
        }}

        .sources-heading {{
            font-size: 0.72rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: {MUTED};
            margin: 1.25rem 0 0.65rem;
        }}

        .source-strip {{
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
            background: {BG};
            border: 1px solid {BORDER};
            border-left: 4px solid {ACCENT};
            border-radius: 10px;
            padding: 0.85rem 1rem;
            margin-bottom: 0.5rem;
            transition: box-shadow 0.15s;
        }}
        .source-strip:hover {{
            box-shadow: 0 2px 12px rgba(15, 23, 42, 0.08);
        }}
        .source-strip.k8s {{ border-left-color: {K8S}; }}
        .source-strip.tf {{ border-left-color: {TF}; }}
        .source-strip .num {{
            font-family: "JetBrains Mono", monospace;
            font-size: 0.75rem;
            font-weight: 600;
            color: {MUTED};
            min-width: 1.5rem;
        }}
        .source-strip .body {{ flex: 1; }}
        .source-strip .tool-tag {{
            font-size: 0.65rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            padding: 0.12rem 0.45rem;
            border-radius: 4px;
            display: inline-block;
            margin-bottom: 0.25rem;
        }}
        .source-strip .tool-tag.k8s {{ background: {K8S_LIGHT}; color: {K8S}; }}
        .source-strip .tool-tag.tf {{ background: {TF_LIGHT}; color: {TF}; }}
        .source-strip .doc-title {{
            font-size: 0.88rem;
            font-weight: 600;
            color: {TEXT};
            line-height: 1.35;
        }}
        .source-strip .doc-section {{
            font-size: 0.78rem;
            color: {MUTED};
            margin-top: 0.15rem;
        }}
        .source-strip a {{
            font-size: 0.75rem;
            color: {ACCENT};
            text-decoration: none;
            font-weight: 600;
            white-space: nowrap;
        }}

        .empty-state {{
            text-align: center;
            padding: 2.5rem 1rem;
            color: {MUTED};
        }}
        .empty-state .icon {{ font-size: 2.5rem; margin-bottom: 0.5rem; opacity: 0.5; }}

        .footer-bar {{
            text-align: center;
            font-size: 0.8rem;
            color: {MUTED};
            margin-top: 2rem;
            padding-top: 1.25rem;
            border-top: 1px solid {BORDER};
        }}
        .footer-bar a {{ color: {ACCENT}; text-decoration: none; font-weight: 600; }}

        /* Streamlit widgets */
        div[data-testid="stTextArea"] textarea {{
            background: {SURFACE} !important;
            border: 2px solid {BORDER} !important;
            border-radius: 14px !important;
            color: {TEXT} !important;
            font-size: 0.95rem !important;
            padding: 0.85rem !important;
        }}
        div[data-testid="stTextArea"] textarea:focus {{
            border-color: {ACCENT} !important;
            box-shadow: 0 0 0 3px rgba(13, 148, 136, 0.15) !important;
        }}
        .stButton > button[kind="primary"] {{
            background: linear-gradient(135deg, {ACCENT}, #0891b2) !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 600 !important;
            padding: 0.6rem 1.5rem !important;
            box-shadow: 0 4px 14px rgba(13, 148, 136, 0.3) !important;
        }}
        .stButton > button[kind="secondary"] {{
            border-radius: 10px !important;
            border: 1px solid {BORDER} !important;
            background: {SURFACE} !important;
            color: {TEXT} !important;
            font-size: 0.82rem !important;
        }}
        section[data-testid="stSidebar"] {{
            background: {SURFACE};
            border-right: 1px solid {BORDER};
        }}
        section[data-testid="stSidebar"] .block-container {{
            padding-top: 1.5rem;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )
