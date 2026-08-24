from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Agentic RAG"
    app_env: str = "production"
    host: str = "0.0.0.0"
    port: int = 10000

    qdrant_collection: str = "software_docs"
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str = ""

    hf_token: str = ""
    hf_model: str = "mistralai/Mistral-7B-Instruct-v0.3"
    hf_base_url: str = "https://router.huggingface.co/v1"
    hf_max_new_tokens: int = 512

    tavily_api_key: str = ""

    embedding_model: str = "BAAI/bge-small-en-v1.5"
    rerank_model: str = "BAAI/bge-reranker-base"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
