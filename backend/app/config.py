"""
Application configuration.

Reads settings from environment variables (or a local .env file).
Keeping all configuration in one place makes it easy to deploy the
same codebase to different environments (local, Render, Railway, etc.)
without changing any code.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database connection string. Defaults to a local SQLite file so the
    # project runs out-of-the-box with zero external setup.
    DATABASE_URL: str = "sqlite:///./timetable.db"

    # Comma-separated list of origins allowed to call this API.
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    # Whether to automatically insert seed data when the database is empty.
    AUTO_SEED: bool = True

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins_list(self) -> list[str]:
        """Turn the comma-separated CORS_ORIGINS string into a clean list."""
        if self.CORS_ORIGINS.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()
