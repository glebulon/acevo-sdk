# acevo-sdk

`acevo-sdk` is a Python SDK for Assetto Corsa Evo log parsing and shared-memory telemetry.

It packages the reusable telemetry foundation extracted from SimLaps so other projects can build on ACE data without reimplementing log parsing, binary decoding, or shared-memory capture.

This is an independent community SDK. It is not official Kunos Simulazioni or Assetto Corsa software.

## Install

```bash
pip install acevo-sdk
```

For local development from this repository:

```bash
python -m pip install -e ".[dev]"
```

## What It Includes

- ACE log parsing for sessions, laps, sectors, validity, player identity, car, track, tyre compound, setup notes, and fuel signals.
- Live shared-memory capture for ACE physics, graphics, and static regions on Windows.
- Decoders for captured shared-memory bytes.
- Reusable dataclasses for laps, sessions, stints, frames, capture metadata, and shared session state.
- Track catalog helpers and bundled track catalog data.

## What It Does Not Include

- SimLaps API submission.
- Discord notifications.
- Personal-best cache.
- Desktop UI.
- Signing, anti-cheat, or server security helpers.
- HTML telemetry reports, AI prompts, or the larger telemetry analyzer pipeline.

Those belong in downstream applications for now.

## Use Cases

- Build lap-tracking apps like SimLaps that parse ACE logs, detect sessions, laps, sectors, validity, and send structured data to a custom backend.
- Capture live shared-memory telemetry for dashboards, overlays, stream widgets, engineering tools, or race-control utilities.
- Decode saved raw shared-memory dumps offline for reverse engineering, debugging, analysis notebooks, or regression tests.
- Build coaching tools that consume lap, sector, car, track, fuel, tyre, and telemetry signals, while keeping AI/report generation in the downstream app.
- Create personal data pipelines that export ACE session data to JSONL, SQLite, DuckDB, Parquet, spreadsheets, or analytics services.
- Build test fixtures and validation tools for ACE telemetry integrations without each project reimplementing log parsing and binary decoding.
- Prototype future setup/tuning tools on top of stable decoded telemetry and catalog APIs.

## Parse Logs

```python
import asyncio
from acevo import LogParser


async def main():
    parser = LogParser()
    sessions = await parser.parse_file()
    for session in sessions:
        print(session.track, session.car, session.best_lap)


asyncio.run(main())
```

You can pass a specific log file or directory:

```python
parser = LogParser(r"C:\Users\you\Saved Games\ACE\Logs")
```

## Capture Shared Memory

Live shared-memory capture is Windows-only because ACE exposes telemetry through Win32 file mappings.

```python
import asyncio
from acevo import TelemetryCapture


async def main():
    capture = TelemetryCapture(hz=20)
    await capture.start_capture()
    await asyncio.sleep(30)
    frames = await capture.stop_capture()
    print(f"captured {len(frames)} frames")


asyncio.run(main())
```

If your application already knows whether the game is running, you can inject a callback:

```python
capture = TelemetryCapture(game_running_callback=lambda: True)
```

When no callback is provided, the SDK does not enforce game-process detection.

## Decode Raw Bytes

```python
from pathlib import Path
from acevo import decode_graphics, decode_static

graphics_bytes = bytes.fromhex(Path("graphics_frame.hex").read_text().strip())
static_bytes = bytes.fromhex(Path("static_frame.hex").read_text().strip())

graphics = decode_graphics(graphics_bytes)
static = decode_static(static_bytes)

print(graphics)
print(static)
```

## Public API

```python
from acevo import (
    LogParser,
    TelemetryCapture,
    RegionReader,
    FrameData,
    CaptureMetadata,
    decode_physics,
    decode_graphics,
    decode_static,
    LapData,
    SessionData,
    LapState,
    SharedSessionManager,
)
```

## Status

`acevo-sdk` is Alpha software. Version `0.1.0` is the first extracted SDK release, so public APIs may change while real downstream use cases settle.

Please report issues at https://github.com/glebulon/acevo-sdk/issues.

## Publishing

This repo is designed for PyPI Trusted Publishing through GitHub Actions.

Release checklist:

```bash
python -m pip install -e ".[dev]"
ruff check .
pytest
python -m build
git tag v0.1.0
git push origin v0.1.0
```

Create the GitHub Release for `v0.1.0`; the publish workflow uploads the package to PyPI.

## License

MIT
