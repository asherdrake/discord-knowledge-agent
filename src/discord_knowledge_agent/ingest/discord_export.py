"""
Discord export parsing (Phase 1).

Purpose:
- Parse a user-provided Discord export JSON into `RawDiscordMessage` objects.

Planned implementation:
- Support common export variants (top-level list or { "messages": [...] }).
- Extract: message_id, created_at, author, channel_id, content, attachments, reply refs.
- Be permissive in parsing, strict in output validation.
"""

