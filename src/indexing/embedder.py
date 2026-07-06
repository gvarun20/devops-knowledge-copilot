"""Local embedding model."""

from sentence_transformers import SentenceTransformer

from src.config import load_settings


class Embedder:
    def __init__(self) -> None:
        cfg = load_settings()["embeddings"]
        self.model = SentenceTransformer(cfg["model_name"])
        self.batch_size = cfg["batch_size"]

    @property
    def dim(self) -> int:
        fn = getattr(self.model, "get_embedding_dimension", None)
        return fn() if fn else self.model.get_sentence_embedding_dimension()

    def encode(self, texts: list[str]) -> list[list[float]]:
        vecs = self.model.encode(
            texts,
            batch_size=self.batch_size,
            normalize_embeddings=True,
            show_progress_bar=len(texts) > self.batch_size,
        )
        return vecs.tolist()
