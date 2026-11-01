import json
import math

import httpx

from app.core.config import settings


class EmbeddingProviderError(RuntimeError):
    """Raised when a configured embedding provider cannot create a vector."""


def _openai_embedding(text: str) -> list[float]:
    if not settings.openai_api_key:
        raise EmbeddingProviderError(
            "OPENAI_API_KEY is required when LLM_PROVIDER=openai."
        )

    url = f"{settings.openai_base_url.rstrip('/')}/embeddings"
    headers = {"Authorization": f"Bearer {settings.openai_api_key}"}
    try:
        with httpx.Client(timeout=settings.llm_timeout_seconds) as client:
            response = client.post(
                url,
                headers=headers,
                json={"model": settings.openai_embedding_model, "input": text},
            )
    except httpx.RequestError as exc:
        raise EmbeddingProviderError("Could not reach the OpenAI embeddings API.") from exc

    if response.is_error:
        try:
            detail = response.json().get("error", {}).get("message", "")
        except (ValueError, AttributeError):
            detail = ""
        raise EmbeddingProviderError(
            f"OpenAI embeddings API returned HTTP {response.status_code}. {detail}".strip()
        )

    try:
        vector = response.json()["data"][0]["embedding"]
        return [float(value) for value in vector]
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise EmbeddingProviderError(
            "OpenAI returned an invalid embeddings response."
        ) from exc


def _bedrock_embedding(text: str) -> list[float]:
    try:
        import boto3

        client = boto3.client("bedrock-runtime", region_name=settings.bedrock_region)
        response = client.invoke_model(
            modelId=settings.bedrock_embedding_model_id,
            body=json.dumps({
                "inputText": text,
                "dimensions": settings.bedrock_embedding_dimensions,
                "normalize": True,
            }),
            accept="application/json",
            contentType="application/json",
        )
        payload = json.loads(response["body"].read())
        vector = payload.get("embedding")
        if vector is None:
            vector = payload.get("embeddingsByType", {}).get("float")
        if not vector:
            raise ValueError("Bedrock response did not contain an embedding.")
        return [float(value) for value in vector]
    except Exception as exc:
        raise EmbeddingProviderError(
            "Amazon Bedrock could not create an embedding. Check AWS credentials, "
            "region, model access, and bedrock:InvokeModel permission."
        ) from exc


def embed_text(text: str) -> list[float]:
    """Create a semantic vector with the configured provider."""
    if not text or not text.strip():
        raise ValueError("Text to embed cannot be empty.")

    provider = settings.llm_provider.lower()
    if provider == "openai":
        vector = _openai_embedding(text)
    elif provider == "bedrock":
        vector = _bedrock_embedding(text)
    else:
        raise EmbeddingProviderError(
            f"Unsupported LLM_PROVIDER '{settings.llm_provider}'. Use 'openai' or 'bedrock'."
        )

    if not vector or not all(math.isfinite(value) for value in vector):
        raise EmbeddingProviderError("The embedding provider returned an invalid vector.")
    return vector


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
