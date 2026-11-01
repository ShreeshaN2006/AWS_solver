from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    api_prefix: str = "/api"

    # OpenAI configuration
    openai_api_key: str = ""
    openai_base_url: str = "https://api.openai.com/v1"
    openai_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"

    # Amazon Bedrock configuration
    bedrock_region: str = "us-east-1"
    bedrock_model_id: str = "amazon.nova-micro-v1:0"
    bedrock_embedding_model_id: str = "amazon.titan-embed-text-v2:0"
    bedrock_embedding_dimensions: int = 1024

    llm_provider: str = "openai"
    llm_timeout_seconds: float = 45.0
    retrieval_min_score: float = 0.20

    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "aws_academy_copilot"
    canvas_base_url: str = "https://awsacademy.instructure.edu"
    canvas_course_id: int = 183194
    canvas_client_id: str = ""
    canvas_client_secret: str = ""
    canvas_redirect_uri: str = "http://localhost:8000/api/integrations/canvas/callback"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
