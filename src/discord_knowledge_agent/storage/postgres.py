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

def list_raw_messages(limit: int | None = None) -> list[RawDiscordMessage]:
  with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
      if limit is None:
        cur.execute('''
          SELECT message_id, channel_id, author_id, content, created_at, reply_to_id
          FROM raw_discord_messages
          ORDER BY created_at ASC;
        ''')
      else:
        cur.execute('''
          SELECT message_id, channel_id, author_id, content, created_at, reply_to_id
          FROM raw_discord_messages
          ORDER BY created_at ASC
          LIMIT %s;
        ''', (limit,))
      rows = cur.fetchall()

  return [
    RawDiscordMessage(
      message_id=r[0],
      channel_id=r[1],
      author_id=r[2],
      content=r[3],
      created_at=r[4],
      reply_to_id=r[5]
    )
    for r in rows
  ]  

def list_uncategorized_messages(limit: int | None = None) -> list[RawDiscordMessage]:
  with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
      if limit is None:
        cur.execute('''
          SELECT R.message_id, R.channel_id, R.author_id, R.content, R.created_at, R.reply_to_id
          FROM raw_discord_messages R
          LEFT JOIN category_assignments C ON R.message_id = C.message_id
          WHERE C.message_id IS NULL
          ORDER BY R.created_at ASC;
        ''')
      else:
        cur.execute('''
          SELECT R.message_id, R.channel_id, R.author_id, R.content, R.created_at, R.reply_to_id
          FROM raw_discord_messages R
          LEFT JOIN category_assignments C ON R.message_id = C.message_id
          WHERE C.message_id IS NULL
          ORDER BY R.created_at ASC
          LIMIT %s;
        ''', (limit,))
      rows = cur.fetchall()

  return [
    RawDiscordMessage(
      message_id=r[0],
      channel_id=r[1],
      author_id=r[2],
      content=r[3],
      created_at=r[4],
      reply_to_id=r[5]
    )
    for r in rows
  ]  

def list_messages_with_assignments(limit: int | None = None) -> list[tuple[RawDiscordMessage, CategoryAssignment]]:
  with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
      if limit is None:
        cur.execute('''
          SELECT R.message_id, R.channel_id, R.author_id, R.content, R.created_at, R.reply_to_id, C.message_id, C.category, C.confidence, C.rationale, C.assigned_at, C.method
          FROM raw_discord_messages R
          INNER JOIN category_assignments C ON R.message_id = C.message_id
          ORDER BY R.created_at ASC;
        ''')
      else:
        cur.execute('''
          SELECT R.message_id, R.channel_id, R.author_id, R.content, R.created_at, R.reply_to_id, C.message_id, C.category, C.confidence, C.rationale, C.assigned_at, C.method
          FROM raw_discord_messages R
          INNER JOIN category_assignments C ON R.message_id = C.message_id
          ORDER BY R.created_at ASC
          LIMIT %s;
        ''', (limit,))
      rows = cur.fetchall()

  return [
    (
      RawDiscordMessage(
        message_id=r[0],
        channel_id=r[1],
        author_id=r[2],
        content=r[3],
        created_at=r[4],
        reply_to_id=r[5]
      ),
      CategoryAssignment(
        message_id=r[6],
        category=r[7],
        confidence=r[8],
        rationale=r[9],
        assigned_at=r[10],
        method=r[11]
      )
    )
    for r in rows
  ]  

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

def list_category_assignments(limit: int | None = None) -> list[CategoryAssignment]:
  with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
      if limit is None:
        cur.execute('''
          SELECT message_id, category, confidence, rationale, assigned_at, method
          FROM category_assignments
          ORDER BY assigned_at ASC;
        ''')
      else:
        cur.execute('''
          SELECT message_id, category, confidence, rationale, assigned_at, method
          FROM category_assignments
          ORDER BY assigned_at ASC
          LIMIT %s;
        ''', (limit,))
      rows = cur.fetchall()

  return [
    CategoryAssignment(
      message_id=r[0],
      category=r[1],
      confidence=r[2],
      rationale=r[3],
      assigned_at=r[4],
      method=r[5]
    )
    for r in rows
  ]  

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

def list_export_ledger_records(limit: int | None = None) -> list[ExportLedgerRecord]:
  with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
      if limit is None:
        cur.execute('''
          SELECT ledger_id, category, target_system, target_document_id, content_hash, status, exported_at
          FROM export_ledger_records
          ORDER BY exported_at ASC;
        ''')
      else:
        cur.execute('''
          SELECT ledger_id, category, target_system, target_document_id, content_hash, status, exported_at
          FROM export_ledger_records
          ORDER BY exported_at ASC
          LIMIT %s;
        ''', (limit,))

      rows = cur.fetchall()

  return [
    ExportLedgerRecord(
      ledger_id=r[0],
      category=r[1],
      target_system=r[2],
      target_document_id=r[3],
      content_hash=r[4],
      status=r[5],
      exported_at=r[6]
    )
    for r in rows
  ]  

def get_latest_export_ledger_record() -> ExportLedgerRecord | None:
  with psycopg.connect(DATABASE_URL) as conn:
    with conn.cursor() as cur:
      cur.execute('''
        SELECT ledger_id, category, target_system, target_document_id, content_hash, status, exported_at
        FROM export_ledger_records
        ORDER BY exported_at DESC
        LIMIT 1;
      ''')
      row = cur.fetchone()

  return ExportLedgerRecord(
            ledger_id=row[0],
            category=row[1],
            target_system=row[2],
            target_document_id=row[3],
            content_hash=row[4],
            status=row[5],
            exported_at=row[6]
          ) if row else None