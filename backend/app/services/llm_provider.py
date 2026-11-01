import httpx

from app.core.config import settings


SYSTEM_INSTRUCTIONS = """You are a patient tutor for a learner studying AWS Academy Cloud Foundations.
Explain concepts clearly, step by step, and define technical terms when needed.
Treat supplied course excerpts as the source of truth for course-specific claims.
Do not invent quotations, module names, page numbers, or course requirements.
When excerpts do not contain enough information, say that the indexed course material
does not answer the question. You may add a clearly labelled general AWS context section,
but do not present general background as if it came from the course.
Never claim to have completed a Canvas quiz, submitted an assessment, or changed an AWS
resource. Keep graded assessment answers under the learner's control."""


class LLMProviderError(RuntimeError):
    """Raised when a configured language-model provider cannot answer."""


class LLMProvider:
    def respond(self, prompt: str, context: str) -> str:  # pragma: no cover - interface
        raise NotImplementedError


class OpenAIProvider(LLMProvider):
    def respond(self, prompt: str, context: str) -> str:
        if not settings.openai_api_key:
            raise LLMProviderError("OPENAI_API_KEY is required when LLM_PROVIDER=openai.")

        user_message = (
            f"Course material excerpts:\n{context or '[No course excerpts were retrieved.]'}"
            f"\n\nLearner question:\n{prompt}"
        )
        try:
            with httpx.Client(timeout=settings.llm_timeout_seconds) as client:
                response = client.post(
                    f"{settings.openai_base_url.rstrip('/')}/chat/completions",
                    headers={"Authorization": f"Bearer {settings.openai_api_key}"},
                    json={
                        "model": settings.openai_model,
                        "messages": [
                            {"role": "system", "content": SYSTEM_INSTRUCTIONS},
                            {"role": "user", "content": user_message},
                        ],
                        "temperature": 0.2,
                    },
                )
        except httpx.RequestError as exc:
            raise LLMProviderError("Could not reach the OpenAI chat API.") from exc

        if response.is_error:
            try:
                detail = response.json().get("error", {}).get("message", "")
            except (ValueError, AttributeError):
                detail = ""
            raise LLMProviderError(
                f"OpenAI chat API returned HTTP {response.status_code}. {detail}".strip()
            )

        try:
            answer = response.json()["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMProviderError(
                "OpenAI returned an invalid chat completion response."
            ) from exc
        if not isinstance(answer, str) or not answer.strip():
            raise LLMProviderError("OpenAI returned an empty tutor response.")
        return answer.strip()


class BedrockProvider(LLMProvider):
    def respond(self, prompt: str, context: str) -> str:
        try:
            import boto3

            client = boto3.client("bedrock-runtime", region_name=settings.bedrock_region)
            user_message = (
                f"Course material excerpts:\n{context or '[No course excerpts were retrieved.]'}"
                f"\n\nLearner question:\n{prompt}"
            )
            response = client.converse(
                modelId=settings.bedrock_model_id,
                system=[{"text": SYSTEM_INSTRUCTIONS}],
                messages=[{"role": "user", "content": [{"text": user_message}]}],
                inferenceConfig={"maxTokens": 1200, "temperature": 0.2},
            )
            blocks = response["output"]["message"]["content"]
            answer = "\n".join(
                block["text"] for block in blocks if isinstance(block, dict) and "text" in block
            )
            if not answer.strip():
                raise ValueError("Bedrock returned no text content.")
            return answer.strip()
        except Exception as exc:
            raise LLMProviderError(
                "Amazon Bedrock could not generate a tutor response. Check AWS credentials, "
                "region, model access, and bedrock:InvokeModel permission."
            ) from exc


def get_llm_provider() -> LLMProvider:
    provider = settings.llm_provider.lower()
    if provider == "bedrock":
        return BedrockProvider()
    if provider == "openai":
        return OpenAIProvider()
    raise LLMProviderError(
        f"Unsupported LLM_PROVIDER '{settings.llm_provider}'. Use 'openai' or 'bedrock'."
    )
