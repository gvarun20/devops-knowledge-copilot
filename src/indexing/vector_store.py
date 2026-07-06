"""Qdrant vector store."""

from __future__ import annotations

import uuid
from typing import Any

from qdrant_client import QdrantClient
from qdrant_client.http import models as qm

from src.config import load_settings
from src.models import Chunk


class VectorStore:
    def __init__(self) -> None:
        cfg = load_settings()["qdrant"]
        self.name = cfg["collection_name"]
        self.client = QdrantClient(host=cfg["host"], port=cfg["port"], check_compatibility=False)

    def reset(self, dim: int) -> None:
        if self.client.collection_exists(self.name):
            self.client.delete_collection(self.name)
        self.client.create_collection(
            collection_name=self.name,
            vectors_config=qm.VectorParams(size=dim, distance=qm.Distance.COSINE),
        )

    @staticmethod
    def _id(chunk_id: str) -> str:
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, chunk_id))

    def upsert(self, chunks: list[Chunk], vectors: list[list[float]]) -> None:
        points = [
            qm.PointStruct(
                id=self._id(c.chunk_id),
                vector=v,
                payload={
                    "chunk_id": c.chunk_id,
                    "tool": c.tool,
                    "document_title": c.document_title,
                    "file_path": c.file_path,
                    "source_url": c.source_url,
                    "section_header": c.section_header,
                    "section_path": c.section_path,
                    "content": c.content,
                    "word_count": c.word_count,
                },
            )
            for c, v in zip(chunks, vectors, strict=True)
        ]
        for i in range(0, len(points), 256):
            self.client.upsert(collection_name=self.name, points=points[i : i + 256])

    def search(self, vector: list[float], top_k: int) -> list[dict[str, Any]]:
        res = self.client.query_points(
            collection_name=self.name,
            query=vector,
            limit=top_k,
            with_payload=True,
        )
        hits: list[dict[str, Any]] = []
        for pt in res.points:
            payload = dict(pt.payload or {})
            payload["score"] = float(pt.score)
            payload["chunk_id"] = payload.get("chunk_id", str(pt.id))
            hits.append(payload)
        return hits
