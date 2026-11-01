from app.core.config import settings
from app.models.schemas import DocumentChunk
from app.services.embeddings import cosine_similarity, embed_text


class RetrievalService:
    def __init__(self) -> None:
        self.chunks: list[DocumentChunk] = []

    def ingest(self, chunks: list[DocumentChunk]) -> None:
        for chunk in chunks:
            if not chunk.embedding:
                raise ValueError("Cannot index a document chunk without an embedding.")
        self.chunks.extend(chunks)

    def search(
        self,
        query: str,
        module_id: str | None = None,
        limit: int = 4,
    ) -> list[DocumentChunk]:
        if limit <= 0 or not query.strip():
            return []

        query_embedding = embed_text(query)
        candidates = [
            chunk
            for chunk in self.chunks
            if (not module_id or chunk.module_id == module_id)
            and len(chunk.embedding) == len(query_embedding)
        ]
        scored = [
            (cosine_similarity(query_embedding, candidate.embedding), candidate)
            for candidate in candidates
        ]
        scored.sort(key=lambda entry: entry[0], reverse=True)
        return [
            chunk
            for score, chunk in scored[:limit]
            if score >= settings.retrieval_min_score
        ]


retrieval_service = RetrievalService()
