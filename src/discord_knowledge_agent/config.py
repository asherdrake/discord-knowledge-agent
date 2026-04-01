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

