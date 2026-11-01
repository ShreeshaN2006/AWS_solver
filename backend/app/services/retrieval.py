from app.models.schemas import DocumentChunk
from app.services.embeddings import cosine_similarity, embed_text


class RetrievalService:
    def __init__(self) -> None:
        self.chunks: list[DocumentChunk] = []

    def ingest(self, chunks: list[DocumentChunk]) -> None:
        self.chunks.extend(chunks)

    def search(self, query: str, module_id: str | None = None, limit: int = 4) -> list[DocumentChunk]:
        query_embedding = embed_text(query)
        candidates = [c for c in self.chunks if not module_id or c.module_id == module_id]
        scored = [
            (cosine_similarity(query_embedding, candidate.embedding), candidate)
            for candidate in candidates
        ]
        scored.sort(key=lambda x: x[0], reverse=True)
        return [entry[1] for entry in scored[:limit] if entry[0] > 0.65]


retrieval_service = RetrievalService()
