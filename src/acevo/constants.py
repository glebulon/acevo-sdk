"""
ACE Log Parser Constants

Tuning constants and configuration values.
"""


# `tyres out → 4` events with inside_distance above this are pit-teleport
# artefacts. All three analysed logs show exactly 12.52 m for teleports;
# real violations are below ±3.5 m.
PIT_TELEPORT_DISTANCE_M: float = 10.0

# Minimum inside_distance for a track limit violation to invalidate a lap.
# Values below this (brief momentary excursions) are tolerated by the game.
# Analysis shows violations < 2m don't invalidate, >= 2.62m do.
TRACK_LIMIT_INVALIDATION_THRESHOLD_M: float = 2.0

# Maximum acceptable difference between (S1+S2+S3) and lap_time_ms.
# Small deltas exist due to sub-millisecond boundary timing; anything larger
# indicates sector/lap desync corruption.
SECTOR_SUM_TOLERANCE_MS: int = 50

# Per-lap fuel above this threshold is a hybrid/ERS spike.
HYBRID_FUEL_THRESHOLD_L: float = 10.0

# How many per-lap spikes before we poison the whole session's reliability flag.
HYBRID_SPIKE_SESSION_THRESHOLD: int = 2

# Minimum reasonable lap distance in hundredmeters to flag a lap as aborted.
# Spa-GP is ~69. Setting low because track length varies; callers can filter.
MIN_FULL_LAP_HUNDREDM: int = 20

# Car models with broken ERS/PHEV fuel accounting.
KNOWN_HYBRID_CARS: frozenset[str] = frozenset({
    "ks_ferrari_296_gtb",
    "ks_ferrari_sf90_stradale",
    "ks_mclaren_artura",
})

# Raw GameModeType → normalised session label.
SESSION_TYPE_MAP: dict[str, str] = {
    "INSTANT_RACE": "RACE",
    "RACE":         "RACE",
    "PRACTICE":     "PRACTICE",
    "TIME_ATTACK":  "TIME_ATTACK",
    "QUALIFYING":   "QUALIFYING",
    "HOTLAP":       "HOTLAP",
    "DRIFT":        "DRIFT",
}

# Modes that use the player-only "On Split start" sector format.
PRACTICE_LIKE: frozenset[str] = frozenset({"PRACTICE", "TIME_ATTACK", "HOTLAP"})

# Modes that use the car-specific "Split completed for car <uuid>" format.
RACE_LIKE: frozenset[str] = frozenset({"RACE", "QUALIFYING"})
