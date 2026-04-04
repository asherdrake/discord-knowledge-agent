"""
PostgreSQL store (Phase 1).

Purpose:
- Minimal persistence for MVP:
  - upsert raw messages
  - list notes for organizing
  - store category assignments
  - store export ledger records

Planned implementation:
- Create tables for raw messages, categorization results, and exports.
- Enforce idempotency via primary keys/unique constraints.
"""
import os
import psycopg
from discord_knowledge_agent.models import RawDiscordMessage, CategoryAssignment, ExportLedgerRecord

DATABASE_URL = os.environ["DATABASE_URL"]
 
def upsert_raw_message(msg: RawDiscordMessage) -> None:
  with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
      cur.execute('''
        INSERT INTO raw_discord_messages (
          message_id,
          channel_id,
          author_id,
          content,
          created_at,
          reply_to_id
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (message_id) DO UPDATE SET
          channel_id = EXCLUDED.channel_id,
          author_id = EXCLUDED.author_id,
          content = EXCLUDED.content,
          created_at = EXCLUDED.created_at,
          reply_to_id = EXCLUDED.reply_to_id;
      ''', (
        msg.message_id,
        msg.channel_id,
        msg.author_id,
        msg.content,
        msg.created_at,
        msg.reply_to_id
      ))

def upsert_category_assignment(assignment: CategoryAssignment) -> None:
  with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
      cur.execute('''
        INSERT INTO category_assignments (
          message_id,
          category,
          confidence,
          rationale,
          assigned_at,
          method
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        ON CONFLICT (message_id) DO UPDATE SET
          category = EXCLUDED.category,
          confidence = EXCLUDED.confidence,
          rationale = EXCLUDED.rationale,
          assigned_at = EXCLUDED.assigned_at,
          method = EXCLUDED.method;
      ''', (
        assignment.message_id,
        assignment.category,
        assignment.confidence,
        assignment.rationale,
        assignment.assigned_at,
        assignment.method
      ))

def insert_export_ledger_record(record: ExportLedgerRecord) -> None:
  with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
      cur.execute('''
        INSERT INTO export_ledger_records (
          ledger_id,
          category,
          target_system,
          target_document_id,
          content_hash,
          status,
          exported_at
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
      ''', (
        record.ledger_id,
        record.category,
        record.target_system,
        record.target_document_id,
        record.content_hash,
        record.status,
        record.exported_at
      ))