import numpy as np
import logging
from typing import List, Dict, Any, Optional
from app.database import get_database
from app.services.llm_provider import get_llm_provider
from app.config import settings

logger = logging.getLogger("app.services.vector_store")

class VectorStore:
    def __init__(self, provider=None):
        # Keep injected providers for tests; otherwise resolve the configured
        # provider when a request runs so Settings changes take effect.
        self._provider = provider

    @property
    def provider(self):
        return self._provider or get_llm_provider()

    async def add_chunks(self, chunks: List[Dict[str, Any]]) -> int:
        """Insert or replace document chunks in MongoDB."""
        db = get_database()
        if not chunks:
            return 0
        
        # Check if chunks already have embeddings, if not generate them
        texts_to_embed = [c["content"] for c in chunks if not c.get("embedding")]
        if texts_to_embed:
            embeddings = await self.provider.get_embeddings(texts_to_embed)
            embed_idx = 0
            for c in chunks:
                if not c.get("embedding"):
                    c["embedding"] = embeddings[embed_idx]
                    embed_idx += 1

        inserted = 0
        for chunk in chunks:
            await db.document_chunks.update_one(
                {"chunk_id": chunk["chunk_id"]},
                {"$set": chunk},
                upsert=True
            )
            inserted += 1
        return inserted

    async def search(
        self,
        query: str,
        course_id: str = "183194",
        module_id: Optional[str] = None,
        top_k: int = 5,
        min_score: float = 0.3
    ) -> List[Dict[str, Any]]:
        """
        Perform semantic similarity retrieval on document chunks.
        Computes cosine similarity between query embedding and stored vectors.
        """
        db = get_database()
        query_embs = await self.provider.get_embeddings([query])
        if not query_embs or len(query_embs) == 0:
            return []
        
        q_vec = np.array(query_embs[0], dtype=np.float32)
        q_norm = np.linalg.norm(q_vec)
        if q_norm == 0:
            return []

        # Build filter query
        filter_query: Dict[str, Any] = {"course_id": course_id}
        if module_id and module_id != "all":
            filter_query["module_id"] = str(module_id)

        # Retrieve candidates from MongoDB
        cursor = db.document_chunks.find(filter_query)
        scored_results = []

        async for doc in cursor:
            emb = doc.get("embedding")
            if not emb:
                continue
            d_vec = np.array(emb, dtype=np.float32)
            d_norm = np.linalg.norm(d_vec)
            if d_norm == 0:
                continue
            
            score = float(np.dot(q_vec, d_vec) / (q_norm * d_norm))
            if score >= min_score:
                scored_results.append({
                    "chunk_id": doc.get("chunk_id"),
                    "course_id": doc.get("course_id"),
                    "module_id": doc.get("module_id"),
                    "module_title": doc.get("module_title"),
                    "learning_item_id": doc.get("learning_item_id"),
                    "document_name": doc.get("document_name"),
                    "page_number": doc.get("page_number"),
                    "timestamp": doc.get("timestamp"),
                    "content": doc.get("content"),
                    "source_url": doc.get("source_url"),
                    "score": round(score, 4)
                })

        # Sort descending by similarity score
        scored_results.sort(key=lambda x: x["score"], reverse=True)
        return scored_results[:top_k]

vector_store = VectorStore()
