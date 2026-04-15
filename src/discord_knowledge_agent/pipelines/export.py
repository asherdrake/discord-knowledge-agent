"""
Export pipeline (Phase 1).

Purpose:
- Load categorized notes and write category docs via the local markdown exporter.

Planned implementation:
- Read category assignments + messages from `storage.postgres`.
- Render markdown via `export.local_md`.
- Record results in an export ledger table for idempotency.
"""
from uuid import uuid4
from discord_knowledge_agent.export.local_md import write_markdown, CategoryExportResult
from discord_knowledge_agent.storage.postgres import insert_export_ledger_record, list_messages_with_assignments
from discord_knowledge_agent.models import RawDiscordMessage, CategoryAssignment, ExportLedgerRecord

# takes a path to output directory, exports all messages with assignments there, 
# and returns # of messages exported per category
def run_export(out_dir: str) -> dict[str, CategoryExportResult]:
    msgs_with_assignments: list[tuple[RawDiscordMessage, CategoryAssignment]] = list_messages_with_assignments()
    export_results: dict[str, CategoryExportResult] = write_markdown(out_dir, msgs_with_assignments)

    # already sorted by category within write_markdown
    for cat, export_result in export_results.items():
        record = ExportLedgerRecord(
            ledger_id=str(uuid4()),
            category=cat,
            target_system="local_md",
            target_document_id=str(export_result.output_path),
            content_hash=export_result.content_hash,
            status="ok",
        )
        insert_export_ledger_record(record)

    return export_results


    