"""
Local markdown exporter (Phase 1).

Purpose:
- Write one markdown document per category to an export directory.

Planned implementation:
- Read category assignments + note contents from storage.
- Render deterministic markdown output.
- Maintain an export ledger (content hash) to avoid rewriting unchanged docs.
"""

