"""
CLI entrypoint (Phase 1).

Purpose:
- Provide minimal commands for running Phase 1 workflows:
  - ingest: load Discord notes (file export first)
  - organize: categorize notes
  - export: write category docs to a destination (local markdown first)

Planned implementation:
- Use Typer for CLI structure.
- Delegate real work to `pipelines/` modules.
"""

