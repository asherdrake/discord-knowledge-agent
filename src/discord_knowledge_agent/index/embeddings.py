"""
Embedding utilities (Phase 2).

Purpose:
- Provide a narrow interface for converting note text into vectors.
- Keep embedding-provider details isolated from pipelines.

Planned implementation:
- Add a concrete embedder backend (e.g., local sentence-transformers or API-based).
- Batch embedding requests for throughput.
- Return stable vector dimensionality for compatibility with vector store schema.
"""
from sentence_transformers import SentenceTransformer
from discord_knowledge_agent.models import RawDiscordMessage

# lazy load
_MODEL: SentenceTransformer | None = None

def _get_model() -> SentenceTransformer:
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    return _MODEL

# takes one string of text and returns its vector embedding
# use for querying
def embed_text(text: str) -> list[float]:
    model = _get_model()
    normalized = text.strip() or "(empty)" # handle empty text
    vec = model.encode(normalized, normalize_embeddings=True)
    return vec.tolist()

# takes multiple RawDiscordMessages 
# returns a dict of their ids mapped to their embeddings
def embed_messages(msgs: list[RawDiscordMessage]) -> dict[str, list[float]]:
    if not msgs:
        return {}

    model = _get_model()
    texts = [((m.content or "").strip() or "(empty)") for m in msgs]
    vecs = model.encode(texts, normalize_embeddings=True)

    return {
        m.message_id: v.tolist() 
        for m, v in zip(msgs, vecs)
    }
