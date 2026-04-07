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

from discord_knowledge_agent.models import RawDiscordMessage


def parse_discrub_export(path: str) -> list[RawDiscordMessage]:
    payload: list[dict] = json.loads(Path(path).read_text(encoding="utf-8"))
