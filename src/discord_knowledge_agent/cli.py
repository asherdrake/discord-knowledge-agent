"""
CLI entrypoint (Phase 1).

Purpose:
- Provide minimal commands for running Phase 1 workflows:
  - ingest: load Discord notes (file export first)
  - organize: categorize notes
  - export: write category docs to a destination (local markdown first)

Planned implementation:
- Use Typer for CLI structure.
- Delegate real work to `pipelines/` modules.
"""

import typer
import psycopg
from discord_knowledge_agent.pipelines.ingest import run_ingest
from discord_knowledge_agent.pipelines.organize import run_organize

app = typer.Typer()


@app.command()
def ingest(export_path: str) -> None:
    """
    Parse Discrub export JSON and upsert messages.
    """
    try:
        count = run_ingest(export_path)
        typer.echo(f"Ingested {count} messages.")
    except psycopg.OperationalError:
        typer.echo(
            "Could not connect to PostgreSQL. Is Docker running and db container up?",
            err=True,
        )
        raise typer.Exit(code=1)

@app.command()
def organize(limit: int | None = None) -> None:
    """
    Categorize uncategorized messages. Limit defaults to None.
    """
    try:
        counts: dict[str, int] = run_organize(limit)
        typer.echo(f"Categorized {counts["messages"]} messages. Created {counts["assignments"]} assignments.")
    except psycopg.OperationalError:
        typer.echo(
            "Could not connect to PostgreSQL. Is Docker running and db container up?",
            err=True,
        )
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
