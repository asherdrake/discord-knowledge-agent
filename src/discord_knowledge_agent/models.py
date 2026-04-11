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

from pydantic import BaseModel, Field, field_validator
from datetime import datetime, timezone
from typing import Optional
from discord_knowledge_agent.organize.category_labels import CATEGORY_SET


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
    rationale: str | None = None
    assigned_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    method: str = "heuristic_v1"

    @field_validator("category")
    @classmethod
    def validate_category(cls, c: str) -> str:
        c = c.strip().lower()
        if c not in CATEGORY_SET:
            raise ValueError(f"Unknown category: {c!r}; allowed={sorted(CATEGORY_SET)}")
        return c

class ExportLedgerRecord(BaseModel):
    ledger_id: str
    category: str
    target_system: str
    target_document_id: str
    content_hash: str
    status: str
    exported_at: datetime

