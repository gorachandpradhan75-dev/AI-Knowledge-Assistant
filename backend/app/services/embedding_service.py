"""
Embedding service used to vectorize text chunks for FAISS storage and
similarity search.

Two providers:
  - "sentence_transformers" -> local, CPU-friendly, no network calls
  - "ollama"                -> delegates to an Ollama embedding model

The local model is lazy-loaded once per process to avoid the (multi-
second) load cost on every request.
"""
from functools import lru_cache

import httpx
import numpy as np

from app.core.config import settings
from app.core.logging_config import logger


@lru_cache
def _load_sentence_transformer():
    from sentence_transformers import SentenceTransformer

    logger.info(
        f"Loading sentence-transformer model: {settings.SENTENCE_TRANSFORMER_MODEL}"
    )
    return SentenceTransformer(settings.SENTENCE_TRANSFORMER_MODEL)


class EmbeddingService:
    def __init__(self) -> None:
        self.provider = settings.EMBEDDING_PROVIDER

    async def embed_texts(self, texts: list[str]) -> np.ndarray:
        """Returns a (len(texts), dim) float32 numpy array, L2-normalized."""
        if self.provider == "ollama":
            return await self._embed_via_ollama(texts)
        return self._embed_via_sentence_transformers(texts)

    async def embed_query(self, text: str) -> np.ndarray:
        vectors = await self.embed_texts([text])
        return vectors[0]

    def _embed_via_sentence_transformers(self, texts: list[str]) -> np.ndarray:
        model = _load_sentence_transformer()
        vectors = model.encode(
            texts,
            normalize_embeddings=True,
            convert_to_numpy=True,
        )
        return vectors.astype("float32")

    async def _embed_via_ollama(self, texts: list[str]) -> np.ndarray:
        url = f"{settings.OLLAMA_BASE_URL}/api/embeddings"
        vectors = []

        async with httpx.AsyncClient(timeout=60) as client:
            for text in texts:
                resp = await client.post(
                    url,
                    json={
                        "model": settings.OLLAMA_EMBED_MODEL,
                        "prompt": text,
                    },
                )
                resp.raise_for_status()
                vectors.append(resp.json()["embedding"])

        arr = np.array(vectors, dtype="float32")

        # normalize so inner-product == cosine similarity
        norms = np.linalg.norm(arr, axis=1, keepdims=True)
        norms[norms == 0] = 1

        return arr / norms


embedding_service = EmbeddingService()