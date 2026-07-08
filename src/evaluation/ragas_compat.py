"""Compatibility shim for ragas 0.4.3 + langchain-community 0.4+.

Ragas imports ChatVertexAI from a path removed in newer langchain-community.
We stub the module before ragas loads so evaluation works without Vertex AI.
"""

from __future__ import annotations

import sys
from types import ModuleType

_STUB = "langchain_community.chat_models.vertexai"

if _STUB not in sys.modules:

    class ChatVertexAI:  # pragma: no cover - import stub only
        """Placeholder; ragas uses this only for isinstance checks."""

    mod = ModuleType(_STUB)
    mod.ChatVertexAI = ChatVertexAI
    sys.modules[_STUB] = mod
