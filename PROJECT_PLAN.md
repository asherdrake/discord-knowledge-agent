# Discord → RAG → GraphRAG → MCP Export Agent

## Problem statement

I capture _all_ personal notes/reminders/ideas/lists in a private Discord server/channel. The data is unstructured and disorganized. Build an autonomous, agentic system that ingests this Discord “data graveyard,” semantically categorizes content, validates decisions for reliability, and exports organized artifacts to Notion or Google Docs.

## Objectives (what “done” means)

- **Ingest** Discord messages reliably and incrementally.
- **Normalize** messages into canonical, queryable note events.
- **Organize** notes into durable categories (multi-label when needed) with evidence grounding.
- **Retrieve** via RAG over a vector database for search and categorization support.
- **Link** related concepts across categories via a GraphRAG layer.
- **Validate** categorizations and summaries with a Critic/Evaluator before committing.
- **Export** curated category documents to Notion/Google Docs via **MCP** tool-use with idempotent writes.
- **Observe + evaluate** behavior with traces, metrics, and regression evals.

## Non-goals (initially)

- Perfect taxonomy from day one (taxonomy will evolve).
- Fully real-time streaming ingestion (batch or periodic is acceptable for early phases).
- A full web UI (CLI + logs is sufficient; UI can come later).

---

## System architecture (data flow diagram description)

### Layered pipeline

**Ingest → Normalize → Index → Organize → Validate → Persist → Export → Observe**

### 1) Discord ingestion

- Pull messages from one or more Discord channels via:
  - Discord API (preferred), or
  - a one-time export file for bootstrapping.
- Store raw events as immutable records (**append-only**).

### 2) Normalization + enrichment

- Convert each Discord message into a canonical `NoteEvent` schema:
  - `message_id`, `timestamp`, `author`, `channel`, `content`, `attachments`, `reply/thread refs`, `edited flag`
- Lightweight cleanup:
  - strip bot/system noise, collapse whitespace, detect code blocks/URLs, optional language detection
- Chunking:
  - treat each short Discord message as atomic
  - chunk long messages by semantic boundaries (newline blocks / headings)
- Compute embeddings for each chunk.

### 3) Retrieval layer (Vector DB)

- Upsert embeddings + metadata into **ChromaDB** (local) or **Pinecone** (hosted).
- Maintain a separate “category index” space:
  - category definitions and exemplars also embedded for assignment and drift control.

### 4) Semantic categorization (Organizer agent)

- Periodically (or on-demand) process new notes:
  - cluster notes (time-windowed + embedding similarity)
  - propose/adjust category labels (taxonomy evolves)
  - assign notes to 1..N categories with calibrated confidence
  - generate structured category summaries grounded in retrieved evidence

### 5) GraphRAG construction (concept graph + cross-links)

- Extract entities/concepts and relations from notes + category summaries.
- Build a graph:
  - nodes: notes, categories, entities, projects, dates
  - edges: `related_to`, `mentions`, `depends_on`, `duplicate_of`, `same_topic`
- Use graph expansion during:
  - retrieval (cross-category recall)
  - export (add “related topics” / backlinks)

### 6) Critic/Evaluator gate (reliability)

- Before committing any categorization/export:
  - verify category coherence and consistency
  - check summaries are supported by evidence (no hallucinated claims)
  - enforce schema/policy constraints and confidence thresholds
- If fail:
  - request revision from Organizer, or route to `needs_review` queue.

### 7) Persistence (system of record)

- Store finalized outputs in durable stores:
  - relational DB (SQLite/Postgres) for run state, mappings, audit
  - vector DB for embeddings + chunk metadata
  - graph DB (Neo4j) or persisted edge store for GraphRAG
- Guarantee idempotency:
  - re-runs do not duplicate exports; writes are ledgered.

### 8) MCP tool-use exports (Notion / Google Docs)

- Integrations live behind **MCP** servers (swap backends without changing agents).
- Export strategy:
  - stable document IDs mapped to category IDs
  - incremental, diff-based updates (avoid rewrite-all)
  - retries/backoff and idempotency keys per tool call

### 9) Observability + evaluation

- Log every decision:
  - inputs, retrieved evidence, proposal, critic verdict, tool calls, final commits
- Track metrics:
  - category stability/drift, critic reject rate, export failures, latency/cost

---

## Technical stack (libraries)

### Orchestration / agents

- **LangChain**: orchestration primitives, retrievers, tool abstractions
- **LangGraph**: stateful agent workflows, branching, retries, HITL nodes
- **Pydantic** (or **pydantic-ai**): strict schemas for proposals and tool I/O

### RAG + storage

- **ChromaDB** (local) or **Pinecone** (hosted): vector store
- **Postgres** (recommended) or SQLite: system-of-record state and audit

### GraphRAG

- **Neo4j** (recommended) for graph persistence and querying
- Alternative: persisted edges + **NetworkX** (works locally; less query-native)

### Ingestion

- Discord:
  - `discord.py` (bot ingestion) or REST ingestion with `requests` (batch)

### Evals / testing / tracing

- **pytest**: unit + integration tests
- Tracing/evals:
  - **LangSmith** (if available) or structured logs + OpenTelemetry-style spans

### Packaging / ops

- Docker for local reproducible stack (Chroma/Neo4j/Postgres)
- `.env` for secrets (never committed)

---

## Phased roadmap (4 phases)

## Phase 1 — MVP (Ingest → Categorize → Export)

**Scope**

- Batch ingestion (Discord export or API pull)
- Canonical schema + durable storage for raw + normalized notes
- Baseline categorization with guardrails:
  - small initial taxonomy (e.g., Health, Projects, Shopping, Reminders, Rants)
  - deterministic heuristics for obvious cases (dates/reminders, shopping list patterns)
- Export to **one** destination (pick Notion _or_ Google Docs first)
- CLI commands: `ingest`, `organize`, `export` + run logs

## Phase 2 — RAG integration (Vector DB + grounded decisions)

**Scope**

- Embed + index notes in ChromaDB/Pinecone with strong metadata design
- Retrieval-driven categorization:
  - embed category definitions + exemplars
  - retrieve similar prior notes to ground assignments
- Category summaries with explicit evidence snippets
- “Search mode” Q&A over notes with citations

## Phase 3 — Agentic tool-use (MCP) + side-effect reliability

**Scope**

- Introduce MCP tools as first-class actions:
  - create/update docs, add sections, set Notion properties, attach links
- Use LangGraph state machine:
  - plan → retrieve → propose → validate → commit → export
- Export ledger:
  - idempotent writes, retry policies, and rate-limit handling
- Incremental “daily digest” updates (notes since last run)

## Phase 4 — Senior-level polish (Critic/Evals + GraphRAG + ops)

**Scope**

- Critic/Evaluator gate:
  - consistency checks, hallucination prevention, confidence thresholds
  - evidence verification for summaries and action items
- GraphRAG:
  - entity + relation extraction
  - incremental graph updates
  - graph expansion for cross-category linking and export “related topics”
- Evaluation harness:
  - hand-labeled test set (~200 notes)
  - metrics: categorization accuracy, stability, critic reject rate, hallucination rate
  - regression tests across prompt/model changes
- Observability:
  - traces, cost metrics, failure dashboards (lightweight acceptable)

---

## Edge case strategy (noise, ambiguity, messy reality)

### Noise filtering (without data loss)

- Detect and down-rank low-signal notes:
  - emojis-only, “ok/lol”, repeated spam, bot/system messages
- Keep raw messages for audit, but set `low_signal=true` to avoid polluting clusters.

### Ambiguity handling (avoid forced single-label)

- Support **multi-label** categories with confidence.
- If confidence < threshold:
  - assign to `Inbox/Unsorted` or `NeedsReview`
  - store top-3 candidates + supporting evidence for later resolution.

### Temporal disambiguation

- Convert relative reminders (“tomorrow”) only when timestamp context supports it.
- Otherwise store unresolved temporal references explicitly (no invented dates).

### Contradictions and duplicates

- Deduplicate with embedding similarity + content hashes.
- If conflicting facts exist, keep both; Critic flags inconsistencies rather than “fixing” history.

### Category explosion control

- Limit new categories per run.
- Merge near-duplicate categories via similarity thresholds + critic approval.
- Periodic consolidation pass.

---

## Resume bullet points (post-completion)

- Built an autonomous knowledge-ops agent that ingests unstructured Discord notes, performs evidence-grounded semantic clustering and categorization with LangChain/LangGraph, and exports incremental, idempotent updates to Notion/Google Docs via MCP tool-use.
- Implemented a RAG + GraphRAG retrieval stack (vector DB + concept graph) enabling cross-topic linking, deduplication, and citation-backed Q&A over thousands of notes; designed chunking/metadata schemas to optimize retrieval quality and scalability.
- Shipped reliability infrastructure for agentic workflows including a critic/evaluator gate, regression eval harness with labeled datasets, and observability (traces, retry ledger, cost metrics) to prevent hallucinated writes and monitor drift.

---

## Cursor prompt context (how to use this file)

- Treat this document as the **source of truth** for architecture and sequencing.
- When implementing, keep integrations behind MCP, and keep categorization decisions **grounded** (with evidence snippets stored alongside outputs).
- Prioritize idempotency + auditability: raw data is immutable; derived outputs are reproducible.
