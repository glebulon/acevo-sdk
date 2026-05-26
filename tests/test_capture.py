from acevo import TelemetryCapture
from acevo.capture import get_default_output_dir


def test_capture_does_not_require_game_running_callback() -> None:
    capture = TelemetryCapture()

    assert capture.is_capturing() is False
    assert capture.get_frame_count() == 0


def test_default_output_dir_uses_acevo_name() -> None:
    assert "ACEVO" in get_default_output_dir()
