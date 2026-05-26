"""Decode saved raw shared-memory hex bytes."""

from pathlib import Path

from acevo import decode_graphics, decode_static


def read_hex(path: str) -> bytes:
    return bytes.fromhex(Path(path).read_text(encoding="utf-8").strip())


graphics = decode_graphics(read_hex("graphics_frame.hex"))
static = decode_static(read_hex("static_frame.hex"))

print(graphics)
print(static)
