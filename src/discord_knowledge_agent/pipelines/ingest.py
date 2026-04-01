"""
Ingest pipeline (Phase 1).

Purpose:
- Parse Discord export JSON and persist raw messages to PostgreSQL.

Planned implementation:
- Call `ingest.discord_export` to parse.
- Validate with `models`.
- Upsert into `storage.postgres`.
"""

