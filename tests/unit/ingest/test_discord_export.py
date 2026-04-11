import json
from pathlib import Path
from datetime import datetime, timezone
from discord_knowledge_agent.ingest.discord_export import parse_discrub_export


def test_parser_happy_path_one_message(tmp_path: Path):
    # Arrange
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

    # Act
    result: list[RawDiscordMessage] = parse_discrub_export(str(export_file))

    # Assert
    assert len(result) == 1
    msg = result[0]
    assert msg.message_id == "1490973084495118366"
    assert msg.channel_id == "561037471593398272"
    assert msg.author_id == "178372690497765376"
    assert msg.created_at == datetime.fromisoformat("2026-04-07T07:14:44.284000+00:00")
    assert msg.created_at.tzinfo == timezone.utc
    assert msg.content == "Practice piano"

# def test_parser_discrub_export_rejects_non_list_top_level_shape_one_message(tmp_path: Path):
#     # Arrange
#     payload = [
#         {
#             "id": "1490973084495118366",
#             "channel_id": "561037471593398272",
#             "author": {
#                 "id": "178372690497765376",
#             },
#             "content": "Practice piano",
#             "timestamp": "2026-04-07T07:14:44.284000+00:00",
#         }
#     ]