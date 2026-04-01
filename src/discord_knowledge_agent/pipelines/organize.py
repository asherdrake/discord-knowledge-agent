"""
Organize pipeline (Phase 1).

Purpose:
- Load raw messages from PostgreSQL, apply heuristic categorization, and store assignments.

Planned implementation:
- Read notes from `storage.postgres`.
- Categorize with `organize.heuristic_categorizer`.
- Persist results back to storage.
"""

