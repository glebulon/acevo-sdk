from acevo import (
    CaptureMetadata,
    FrameData,
    LapData,
    LapState,
    LogParser,
    RegionReader,
    SessionData,
    SharedSessionManager,
    TelemetryCapture,
    __version__,
    decode_graphics,
    decode_physics,
    decode_static,
)


def test_public_api_imports() -> None:
    assert __version__ == "0.1.0"
    assert LogParser is not None
    assert TelemetryCapture is not None
    assert RegionReader is not None
    assert FrameData is not None
    assert CaptureMetadata is not None
    assert decode_physics is not None
    assert decode_graphics is not None
    assert decode_static is not None
    assert LapData is not None
    assert SessionData is not None
    assert LapState.PUSH.value == "PUSH"
    assert SharedSessionManager is not None
