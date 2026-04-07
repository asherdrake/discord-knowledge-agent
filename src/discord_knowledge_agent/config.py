"""
Configuration (Phase 1).

Purpose:
- Centralize environment/config settings used by pipelines:
  - database URL (PostgreSQL)
  - export directory
  - (optional later) Discord token + channel IDs

Planned implementation:
- Use `pydantic-settings` to load `.env` and environment variables.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    export_dir: str = "exports"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
