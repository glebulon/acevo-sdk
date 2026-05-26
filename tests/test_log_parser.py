from pathlib import Path

import pytest

from acevo import LogParser


@pytest.mark.asyncio
async def test_parse_sample_log_returns_sessions() -> None:
    log_path = Path(__file__).parent / "fixtures" / "sample_log.txt"
    parser = LogParser(str(log_path))

    sessions = await parser.parse_file()

    assert isinstance(sessions, list)
    assert parser.context.game_version != "Unknown"
