"""
Vector store access layer (Phase 2).

Purpose:
- Encapsulate vector DB operations (upsert/query) behind a simple API.
- Keep pipeline logic independent of vector database vendor specifics.

Planned implementation:
- Initialize and manage a local Chroma collection for note vectors.
- Upsert vectors with metadata for retrieval and citation output.
- Query top-k nearest neighbors by embedding.
"""
