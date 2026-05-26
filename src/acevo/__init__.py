"""Python SDK for Assetto Corsa Evo telemetry and logs."""

from .capture import CaptureMetadata, FrameData, RegionReader, TelemetryCapture
from .decoder import decode_graphics, decode_physics, decode_static
from .logs import LogParser
from .models import InProgressLap, LapData, LapState, SessionData, StintData
from .shared_session import SharedSessionManager

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "CaptureMetadata",
    "FrameData",
    "RegionReader",
    "TelemetryCapture",
    "decode_graphics",
    "decode_physics",
    "decode_static",
    "LogParser",
    "InProgressLap",
    "LapData",
    "LapState",
    "SessionData",
    "StintData",
    "SharedSessionManager",
]
