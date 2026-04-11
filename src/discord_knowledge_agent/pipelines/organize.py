"""
Organize pipeline (Phase 1).

Purpose:
- Load raw messages from PostgreSQL, apply heuristic categorization, and store assignments.

Planned implementation:
- Read notes from `storage.postgres`.
- Categorize with `organize.heuristic_categorizer`.
- Persist results back to storage.
"""
from discord_knowledge_agent.models import RawDiscordMessage, CategoryAssignment
from discord_knowledge_agent.storage.postgres import list_uncategorized_messages, upsert_category_assignment
from discord_knowledge_agent.organize.heuristic_categorizer import categorize_message

def run_organize(limit: int | None = None) -> dict[str, int]:
    uncat_msgs: list[RawDiscordMessage] = list_uncategorized_messages(limit)

    count = 0
    for msg in uncat_msgs:
        cats: list[CategoryAssignment] = categorize_message(msg)
        for cat in cats:
            upsert_category_assignment(cat)
        count += len(cats)
    
    return {
        "messages": len(uncat_msgs), 
        "assignments": count
    }