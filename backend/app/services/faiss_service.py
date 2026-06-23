"""
FAISS-backed vector store.

Design choice: one FAISS index file per document, stored on disk under
FAISS_INDEX_DIR and referenced from the documents collection.
"""
from pathlib import Path

import faiss
import numpy as np

from app.core.config import settings
from app.core.logging_config import logger
from app.db.mongodb import get_database
from app.services.embedding_service import embedding_service


class FaissService:
    def __init__(self) -> None:
        self.index_dir = Path(settings.FAISS_INDEX_DIR)
        self.index_dir.mkdir(parents=True, exist_ok=True)

    def _index_path(self, document_id: str) -> Path:
        return self.index_dir / f"{document_id}.index"

    async def build_index(self, document_id: str, chunks: list[str]) -> str:
        vectors = await embedding_service.embed_texts(chunks)
        dim = vectors.shape[1]

        index = faiss.IndexFlatIP(dim)
        index.add(vectors)

        index_path = self._index_path(document_id)
        faiss.write_index(index, str(index_path))

        db = get_database()

        docs = [
            {
                "document_id": document_id,
                "chunk_index": i,
                "text": chunk,
            }
            for i, chunk in enumerate(chunks)
        ]

        if docs:
            await db.embeddings.delete_many({"document_id": document_id})
            await db.embeddings.insert_many(docs)

        logger.info(
            f"Built FAISS index for document {document_id}: "
            f"{len(chunks)} chunks, dim={dim}"
        )

        return str(index_path)

    async def search(
        self,
        document_id: str,
        query: str,
        top_k: int = 4,
    ) -> list[dict]:

        index_path = self._index_path(document_id)

        if not index_path.exists():
            raise FileNotFoundError(
                f"No FAISS index found for document {document_id}"
            )

        index = faiss.read_index(str(index_path))

        query_vector = await embedding_service.embed_query(query)
        query_vector = np.expand_dims(query_vector, axis=0)

        scores, indices = index.search(
            query_vector,
            min(top_k, index.ntotal),
        )

        db = get_database()

        results = []

        for rank, idx in enumerate(indices[0]):
            if idx == -1:
                continue

            chunk_doc = await db.embeddings.find_one(
                {
                    "document_id": document_id,
                    "chunk_index": int(idx),
                }
            )

            if chunk_doc:
                results.append(
                    {
                        "chunk_index": int(idx),
                        "text": chunk_doc["text"],
                        "score": float(scores[0][rank]),
                    }
                )

        return results

    def delete_index(self, document_id: str) -> None:
        index_path = self._index_path(document_id)

        if index_path.exists():
            index_path.unlink()


faiss_service = FaissService()