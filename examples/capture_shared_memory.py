"""Capture live Assetto Corsa Evo shared-memory telemetry."""

import asyncio

from acevo import TelemetryCapture


async def main() -> None:
    capture = TelemetryCapture(hz=20)
    await capture.start_capture()
    await asyncio.sleep(30)
    frames = await capture.stop_capture()
    print(f"captured {len(frames)} frames")


if __name__ == "__main__":
    asyncio.run(main())
