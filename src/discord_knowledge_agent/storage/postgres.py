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

DATABASE_URL = os.environ["DATABASE_URL"]
 
with psycopg.connect(DATABASE_URL) as conn:
  with conn.cursor() as cur:
    cur.execute("SELECT 1")