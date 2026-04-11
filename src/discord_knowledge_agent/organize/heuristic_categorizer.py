"""
Heuristic categorizer (Phase 1).

Purpose:
- Deterministic baseline categorizer (no LLM required for MVP).

Planned implementation:
- Rules-based assignment into a small taxonomy (e.g., Shopping/Reminders/Health/Projects/Inbox).
- Optional multi-label assignment for ambiguous notes.
- Output confidence + rationale fields (even if heuristic).
"""
from discord_knowledge_agent.models import RawDiscordMessage, CategoryAssignment
from discord_knowledge_agent.organize.category_labels import DEFAULT_CATEGORY

KEYWORDS_BY_CATEGORY: dict[str, tuple[str, ...]] = {
    "goals/reminders": ('todo', 'to-do', 'goals', 'remember', 'do', 'do not', 'make sure'),
    "music": ('listen', 'play', 'piano', 'guitar', 'transcribe', 'practice', 'scales'),
    "computer science": ('project', 'apply', "leetcode", "OA", 'AI'),
    "fitness": ('run', 'gym', 'eat')
}


def categorize_message(msg: RawDiscordMessage) -> list[CategoryAssignment]:
    text = msg.content.strip().lower()

    hits: dict[str, list[str]] = {}
    for category, keywords in KEYWORDS_BY_CATEGORY.items():
        matched_keywords: list[str] = []
        for kw in keywords:
            if kw in text:
                matched_keywords.append(kw)
        if matched_keywords:
            hits[category] = matched_keywords
    
    categorizations: list[CategoryAssignment] = []
    for category, matched_keywords in hits.items():
        assignment = CategoryAssignment(
            message_id=msg.message_id,
            category=category,
            confidence=0.85,
            rationale="matched: " + ", ".join(matched_keywords),
            method="heuristic_v1"
            # omitted assigned_at so default factory takes over
        )
        categorizations.append(assignment)

    if not categorizations:
        categorizations.append(
            CategoryAssignment(
                message_id=msg.message_id,
                category=DEFAULT_CATEGORY,
                confidence=0.4,
                rationale="no keywords matched",
                method="heuristic_v1"
            )
        )
    
    return categorizations

        
