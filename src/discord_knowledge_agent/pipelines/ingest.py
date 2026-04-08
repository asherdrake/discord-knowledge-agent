"""
Ingest pipeline (Phase 1).

Purpose:
- Parse Discord export JSON and persist raw messages to PostgreSQL.

Planned implementation:
- Call `ingest.discord_export` to parse.
- Validate with `models`.
- Upsert into `storage.postgres`.
"""

from discord_knowledge_agent.models import RawDiscordMessage
from discord_knowledge_agent.ingest.discord_export import parse_discrub_export
from discord_knowledge_agent.storage.postgres import upsert_raw_message


# takes a path to Discrub JSON file, upserts messages and returns # of msgs upserted
def run_ingest(export_path: str) -> int:
    messages: list[RawDiscordMessage] = parse_discrub_export(export_path)
    count = 0
    for m in messages:
        upsert_raw_message(m)
        count += 1

    return count
