"""
Index pipeline (Phase 2).

Purpose:
- Read persisted notes from PostgreSQL and index them into a vector store.
- Provide the foundation for retrieval-powered search and categorization.

Planned implementation:
- Load raw messages from `storage.postgres`.
- Embed message content via `index.embeddings`.
- Upsert vectors and metadata via `index.vector_store`.
"""
