"""
Centralized application configuration.

All environment-driven settings live here so the rest of the codebase
never reads `os.environ` directly. This keeps configuration testable
and makes it obvious what knobs exist for deployment.
"""
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ---- App ----
    APP_NAME: str = "AI Knowledge Assistant"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # ---- Security ----
    JWT_SECRET_KEY: str = "CHANGE_ME_super_secret_random_string"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ---- MongoDB ----
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "ai_knowledge_assistant"

    # ---- LLM provider ----
    LLM_PROVIDER: str = "ollama"  # "ollama" | "openai_compatible"
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_CHAT_MODEL: str = "llama3"
    OLLAMA_EMBED_MODEL: str = "nomic-embed-text"
    OPENAI_COMPATIBLE_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_COMPATIBLE_API_KEY: str = ""
    OPENAI_COMPATIBLE_MODEL: str = "gpt-4o-mini"

    # ---- Embeddings ----
    EMBEDDING_PROVIDER: str = "sentence_transformers"
    SENTENCE_TRANSFORMER_MODEL: str = "all-MiniLM-L6-v2"

    # ---- FAISS / storage ----
    FAISS_INDEX_DIR: str = "./storage/faiss_indexes"
    UPLOAD_DIR: str = "./storage/uploads"

    # ---- Web search ----
    WEB_SEARCH_PROVIDER: str = "tavily"  # "tavily" | "serpapi" | "mock"
    TAVILY_API_KEY: str = ""
    SERPAPI_API_KEY: str = ""

    # ---- Voice ----
    WHISPER_MODEL_SIZE: str = "base"

    # ---- Rate limiting ----
    RATE_LIMIT_PER_MINUTE: int = 60

    # ---- Logging ----
    LOG_LEVEL: str = "INFO"
    LOG_DIR: str = "./logs"

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=True, extra="ignore")


@lru_cache
def get_settings() -> Settings:
    """Cached settings accessor — avoids re-parsing the .env on every call."""
    return Settings()


settings = get_settings()