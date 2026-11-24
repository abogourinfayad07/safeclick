"""Configuration de l'API, exclusivement via variables d'environnement."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Valeurs lues depuis l'environnement ou un fichier .env local."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    site_url: str = "http://localhost:3000"
    email_backend: str = "console"

    database_url: str = "sqlite:///./data/safeclick.db"
    redis_url: str = "redis://localhost:6379/0"

    # Valeur de développement uniquement : à remplacer dans .env avant toute mise en ligne.
    secret_key: str = Field(
        default="dev-only-placeholder-not-a-secret",
        description="Clé de signature, à remplacer par une valeur aléatoire en production.",
    )
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    # Limitation en mémoire, suffisante pour une instance. Mettre à false uniquement
    # dans des tests isolés ou derrière un proxy applicatif dédié.
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 60

    @property
    def is_development(self) -> bool:
        return self.environment == "development"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
