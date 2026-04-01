"""
Storage layer (Phase 1).

Purpose:
- Provide a minimal system-of-record for:
  - raw messages (immutable)
  - categorization results
  - export ledger (idempotency + audit)

Phase 1:
- PostgreSQL-backed store.
"""

