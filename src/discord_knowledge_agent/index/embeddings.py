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

# lazy load
_MODEL: SentenceTransformer | None = None

def _get_model() -> SentenceTransformer:
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    return _MODEL