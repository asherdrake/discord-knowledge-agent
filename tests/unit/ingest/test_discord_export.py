import json
from discord_knowledge_agent.ingest.discord_export import parse_discrub_export


def parser_happy_path_one_message(tmp_path):
    payload = [
        {
            "id": "1490973084495118366",
            "channel_id": "561037471593398272",
            "author": {
                "id": "178372690497765376",
            },
            "content": "Practice piano",
            "timestamp": "2026-04-07T07:14:44.284000+00:00",
        }
    ]

    export_file = tmp_path / "export.json"
    export_file.write_text(json.dumps(payload), encoding="utf-8")
