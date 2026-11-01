from app.core.config import settings


class LLMProvider:
    def respond(self, prompt: str, context: str) -> str:  # pragma: no cover - interface stub
        raise NotImplementedError


class OpenAIProvider(LLMProvider):
    def respond(self, prompt: str, context: str) -> str:
        return f"[OpenAI simulated response]\nQuestion: {prompt}\nContext: {context[:500]}"


class BedrockProvider(LLMProvider):
    def respond(self, prompt: str, context: str) -> str:
        return f"[Bedrock simulated response]\nQuestion: {prompt}\nContext: {context[:500]}"


def get_llm_provider() -> LLMProvider:
    if settings.llm_provider.lower() == "bedrock":
        return BedrockProvider()
    return OpenAIProvider()
