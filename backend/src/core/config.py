from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # API Keys
    openai_api_key: str
    tavily_api_key: str
    google_api_key: str

    # Model settings
    openai_model: str = "gpt-4o-mini"
    embedding_model: str = "models/embedding-001"

    # Vectorstore
    collection_name: str = "adaptive_rag_docs"

    # App
    app_name: str = "Adaptive RAG API"
    app_version: str = "0.1.0"
    backend_url: str = "http://localhost:8000"


settings = Settings()