-- RawDiscordMessage
CREATE TABLE IF NOT EXISTS raw_discord_messages (
    message_id      TEXT PRIMARY KEY,
    channel_id      TEXT NOT NULL,
    author_id       TEXT NOT NULL,
    content         TEXT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL,
    reply_to_id     TEXT
);

CREATE TABLE IF NOT EXISTS category_assignments (
    message_id      TEXT PRIMARY KEY REFERENCES raw_discord_messages (message_id) ON DELETE CASCADE,
    category        TEXT NOT NULL,
    confidence      FLOAT NOT NULL,
    rationale       TEXT,
    assigned_at     TIMESTAMPTZ NOT NULL,
    method          TEXT NOT NULL DEFAULT 'heuristic_v1'
);

CREATE TABLE IF NOT EXISTS export_ledger_records (
    ledger_id           TEXT PRIMARY KEY,
    category            TEXT NOT NULL,
    target_system       TEXT NOT NULL,
    target_document_id: TEXT NOT NULL,
    content_hash:       TEXT NOT NULL,
    status:             TEXT NOT NULL,
    exported_at:        TIMESTAMPTZ NOT NULL
);