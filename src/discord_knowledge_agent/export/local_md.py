"""
Local markdown exporter (Phase 1).

Purpose:
- Write one markdown document per category to an export directory.

Planned implementation:
- Read category assignments + note contents from storage.
- Render deterministic markdown output.
- Maintain an export ledger (content hash) to avoid rewriting unchanged docs.
"""
import hashlib
from collections import defaultdict
from pathlib import Path
from discord_knowledge_agent.models import RawDiscordMessage, CategoryAssignment
from dataclasses import dataclass

@dataclass(frozen=True)
class CategoryExportResult:
    content_hash: str
    message_count: int
    output_path: Path

def write_markdown(out_dir: str, msgs_with_assignments: list[tuple[RawDiscordMessage, CategoryAssignment]]) -> dict[str, CategoryExportResult]:
    by_category: dict[str, list[RawDiscordMessage]] = defaultdict(list)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for msg, assignment in msgs_with_assignments:
        by_category[assignment.category].append(msg)
    
    # save content hashes for ExportLedgerRecords
    export_results: dict[str, CategoryExportResult] = {}

    # sort by categories so that output order is stable
    for category, msgs in sorted(by_category.items(), key=lambda x: x[0]):
        msgs.sort(key=lambda x: x.created_at)

        lines: list[str] = []
        lines.append(f"# {category}")
        lines.append("")
        for msg in msgs:
            lines.append(f"## {msg.created_at.isoformat()} - `{msg.message_id}`")
            lines.append("")
            lines.append(msg.content or "")
            lines.append("")

        body = "\n".join(lines).rstrip() + "\n"
        path = out_dir / category_to_filename(category)
        path.write_text(body, encoding="utf-8")

        export_results[category] = CategoryExportResult(
            content_hash=hashlib.sha256(body.encode("utf-8")).hexdigest(),
            message_count=len(msgs),
            output_path=path
        )

    return export_results

def category_to_filename(category: str) -> str:
    safe = category.replace("/", "-").replace(" ", "-")
    return f"{safe}.md"


