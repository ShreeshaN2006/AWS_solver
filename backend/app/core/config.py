from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "development"
    api_prefix: str = "/api"
    openai_api_key: str = ""
    bedrock_region: str = "us-east-1"
    llm_provider: str = "openai"
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_db: str = "aws_academy_copilot"
    canvas_base_url: str = "https://awsacademy.instructure.com"
    canvas_course_id: int = 183194
    canvas_client_id: str = ""
    canvas_client_secret: str = ""
    canvas_redirect_uri: str = "http://localhost:8000/api/integrations/canvas/callback"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
