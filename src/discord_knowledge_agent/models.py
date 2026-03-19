"""
Domain schemas (Phase 1).

Purpose:
- Define canonical models for boundaries between modules:
  - RawDiscordMessage: immutable ingestion record
  - CategoryAssignment / CategorizationResult: organization outputs
  - ExportLedgerRecord: track exports for idempotency

Planned implementation:
- Use Pydantic models for strict validation.
- Keep models stable and extensible (support `extra` metadata).
"""

