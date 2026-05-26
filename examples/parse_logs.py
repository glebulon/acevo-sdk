"""Parse Assetto Corsa Evo logs into structured sessions."""

import asyncio
from pathlib import Path

from acevo import LogParser


async def main() -> None:
    parser = LogParser(str(Path.home() / "Saved Games" / "ACE" / "Logs"))
    sessions = await parser.parse_file()
    for session in sessions:
        best_lap = session.best_lap.lap_time_str if session.best_lap else "none"
        print(f"{session.track} | {session.car} | best={best_lap}")


if __name__ == "__main__":
    asyncio.run(main())
