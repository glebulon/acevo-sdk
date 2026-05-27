from pathlib import Path

from acevo import decode_graphics, decode_static

FIXTURES = Path(__file__).parent / "fixtures"


def _fixture_bytes(name: str) -> bytes:
    return bytes.fromhex((FIXTURES / name).read_text(encoding="utf-8").strip())


def test_decode_graphics_fixture() -> None:
    decoded = decode_graphics(_fixture_bytes("ac_evo_graphics_frame.txt"))

    assert decoded["_decoder"] == "ac_evo_graphics"
    assert decoded["driver_name"] == "Glebulon"
    assert decoded["car_model"] == "Dallara EXP"


def test_decode_static_fixture() -> None:
    decoded = decode_static(_fixture_bytes("ac_evo_static_frame.txt"))

    assert decoded["_decoder"] == "ac_evo_static"
    assert decoded["track"] == "Brands Hatch"
    assert decoded["track_configuration"] == "Indy"
