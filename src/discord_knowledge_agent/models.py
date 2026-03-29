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

from pydantic import BaseModel, Field
from datetime import datetime

class RawDiscordMessage(BaseModel):
  message_id: str
  channel_id: str
  author_id: str
  content: str
  created_at: datetime
  reply_to_id: Optional[str] = None

class CategoryAssignment(BaseModel):
  message_id: str = Field(min_length=1)
  category: str = Field(min_length=1)
  confidence: float = Field(ge=0.0, le=1.0)
  rational: str | None = None
  assigned_at: datetime = Field(
    default_factory=lambda: datetime.now(timezone.utc)
  )
  method: str = "heuristic_v1"
