"""
Export pipeline (Phase 1).

Purpose:
- Load categorized notes and write category docs via the local markdown exporter.

Planned implementation:
- Read category assignments + messages from `storage.postgres`.
- Render markdown via `export.local_md`.
- Record results in an export ledger table for idempotency.
"""

