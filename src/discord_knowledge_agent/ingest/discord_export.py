"""
Discord export parsing (Phase 1).

Purpose:
- Parse a user-provided Discord export JSON into `RawDiscordMessage` objects.

Planned implementation:
- Support common export variants (top-level list or { "messages": [...] }).
- Extract: message_id, created_at, author, channel_id, content, attachments, reply refs.
- Be permissive in parsing, strict in output validation.
"""

import json
from pathlib import Path
from datetime import datetime

from discord_knowledge_agent.models import RawDiscordMessage


def parse_discrub_export(path: str) -> list[RawDiscordMessage]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))

    if not isinstance(payload, list):
        raise ValueError("Expected top-level list")

    parsed_list = [
        RawDiscordMessage(
            message_id=str(msg["id"]),
            channel_id=str(msg["channel_id"]),
            author_id=str(msg["author"]["id"]),
            content=str(msg.get("content", "")),
            created_at=datetime.fromisoformat(msg["timestamp"]),
        )
        for msg in payload
    ]
    return parsed_list
