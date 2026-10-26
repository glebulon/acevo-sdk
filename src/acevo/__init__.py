"""Python SDK for Assetto Corsa Evo telemetry and logs."""

from .capture import (
    CaptureMetadata,
    CaptureSnapshot,
    FrameData,
    LapBoundary,
    RegionReader,
    TelemetryCapture,
)
from .constants import is_hybrid_car
from .context import LogContext
from .decoder import (
    GRAPHICS_SHM_SIZE,
    PHYSICS_SHM_SIZE,
    STATIC_SHM_SIZE,
    decode_graphics,
    decode_physics,
    decode_static,
    peek_graphics_validity,
)
from .logs import LogParser
from .models import InProgressLap, LapData, LapState, SessionData, StintData
from .shared_session import (
    FuelData,
    LapCompletionData,
    LapTimingData,
    LapValidityData,
    PlayerIdentificationData,
    SectorSplitData,
    SessionMetadataData,
    SharedSessionData,
    SharedSessionManager,
    SubmissionFallbackSnapshot,
)
from .tyre_state import TyreState

__version__ = "0.2.1"

__all__ = [
    "__version__",
    "CaptureMetadata",
    "CaptureSnapshot",
    "FrameData",
    "FuelData",
    "InProgressLap",
    "LapBoundary",
    "LapCompletionData",
    "LapData",
    "LapState",
    "LapTimingData",
    "LapValidityData",
    "LogContext",
    "LogParser",
    "PlayerIdentificationData",
    "RegionReader",
    "SectorSplitData",
    "SessionData",
    "SessionMetadataData",
    "SharedSessionData",
    "SharedSessionManager",
    "StintData",
    "SubmissionFallbackSnapshot",
    "TelemetryCapture",
    "TyreState",
    "GRAPHICS_SHM_SIZE",
    "PHYSICS_SHM_SIZE",
    "STATIC_SHM_SIZE",
    "decode_graphics",
    "decode_physics",
    "decode_static",
    "is_hybrid_car",
    "peek_graphics_validity",
]
