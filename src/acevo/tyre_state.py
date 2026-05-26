"""
ACE Log Parser Tyre State Tracker

Tracks compound per position (0=FL, 1=FR, 2=RL, 3=RR).
"""


class TyreState:
    """Tracks compound per position (0=FL, 1=FR, 2=RL, 3=RR).

    Each position is set independently; the final resolved name handles mixed
    setups (seen in practice sessions where the player changes one axle at a
    time through the UI).
    """

    def __init__(self) -> None:
        self._compounds: dict[int, str] = {}

    def set(self, pos: int, code: str) -> None:
        """Set compound for a specific tire position."""
        self._compounds[pos] = code

    def set_all(self, code: str) -> None:
        """Set all 4 tires to the same compound."""
        self._compounds = {0: code, 1: code, 2: code, 3: code}

    def reset(self) -> None:
        self._compounds.clear()

    @property
    def compound_name(self) -> str:
        if not self._compounds:
            return "Unknown"
        codes = set(self._compounds.values())
        if len(codes) == 1:
            return next(iter(codes))
        names = sorted(codes)
        return f"Mixed ({'/'.join(names)})"

    @property
    def compound_code(self) -> str:
        if not self._compounds:
            return "Unknown"
        codes = set(self._compounds.values())
        return next(iter(codes)) if len(codes) == 1 else "Mixed"

    def snapshot(self) -> "TyreState":
        """Return an immutable copy for stint/lap records."""
        copy = TyreState()
        copy._compounds = dict(self._compounds)
        return copy
