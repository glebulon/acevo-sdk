"""Regression tests for race-weekend sub-session type detection.

A ``GameModeType_RACE_WEEKEND`` weekend emits ``Game Started!`` only once;
each subsequent sub-session announces itself with a ``<ModeClass> <Name>
created`` line (e.g. ``InstantRaceRemote Race created``).  Without treating
those as session boundaries, post-practice laps land in the ``connect``-
line fallback session whose type is ``UNKNOWN``.
"""

from acevo.logs import LogParser

STEAM_ID = "76561198321627695"
CAR_UUID = "49a44b2eac12c534-159ad78acd74a2a3"

GAME_STARTED = (
    "[2026-11-07 23:50:18.449] [gameplay] [info] Game Started! "
    "GameModeType_RACE_WEEKEND | Suzuka East Time Attack Practice  "
    "600 seconds @2014/8/15 9:40:0, Qualifying  900 seconds @2014/8/15 "
    "10:5:0, Warmup  600 seconds @2014/8/15 10:35:0, Race  12 laps "
    "@2014/8/15 11:0:0 | ks_abarth_695_biposto | "
    "GameModeSelectionWeatherType_OVERCAST"
)
PLAYER_CONNECT = (
    "[2026-11-07 23:50:24.393] [gameplay] [info] "
    f"{STEAM_ID} connected (true) on car ks_abarth_695_biposto, "
    f"with new carId {CAR_UUID}"
)
PRACTICE_CREATED = (
    "[2026-11-07 23:50:18.571] [gameplay] [info] "
    "TimeAttackRemote Practice created"
)
QUALIFYING_CREATED = (
    "[2026-11-07 23:50:34.063] [gameplay] [info] "
    "TimeAttackRemote Qualifying created"
)
WARMUP_CREATED = (
    "[2026-11-08 00:06:24.320] [gameplay] [info] "
    "TimeAttackRemote Warmup created"
)
WARMUP_CONNECT = (
    "[2026-11-08 00:06:24.932] [gameplay] [info] "
    f"{STEAM_ID} connected (true) on car ks_abarth_695_biposto, "
    f"with new carId {CAR_UUID}"
)
RACE_CREATED = (
    "[2026-11-08 00:09:07.962] [gameplay] [info] "
    "InstantRaceRemote Race created"
)
RACE_CONNECT = (
    "[2026-11-08 00:09:08.454] [gameplay] [info] "
    f"{STEAM_ID} connected (true) on car ks_abarth_695_biposto, "
    f"with new carId {CAR_UUID}"
)
END_SESSION = (
    "[2026-11-08 00:06:01.572] [gameplay] [info] "
    f"END_SESSION Ending Lap for {CAR_UUID} car"
)
EXIT = (
    "[2026-11-08 00:25:53.080] [gameface] [info] "
    "request made GameModeRequestExit "
)


def _new_lap(ts: str, lap: str) -> str:
    return f"[{ts}] [gameplay] [info] New lap carId {CAR_UUID}: {lap}"


class TestRaceWeekendSubSessions:
    def test_created_lines_set_subsession_types(self):
        parser = LogParser()
        parser._process_line(GAME_STARTED)
        parser._process_line(PRACTICE_CREATED)
        parser._process_line(PLAYER_CONNECT)
        assert parser.current_session is not None
        assert parser.current_session.session_type == "PRACTICE"

        parser._process_line(QUALIFYING_CREATED)
        assert parser.current_session.session_type == "QUALIFYING"

        parser._process_line(WARMUP_CREATED)
        assert parser.current_session.session_type == "WARMUP"

        parser._process_line(RACE_CREATED)
        assert parser.current_session.session_type == "RACE"
        assert parser.current_session.track == "Suzuka East"
        assert parser.current_session.car == "ks_abarth_695_biposto"

    def test_subsession_laps_are_not_unknown(self):
        """Laps after a sub-session boundary must not land in the 'UNKNOWN'
        connect-fallback session (the reported bug)."""
        parser = LogParser()
        parser._process_line(GAME_STARTED)
        parser._process_line(PRACTICE_CREATED)
        parser._process_line(PLAYER_CONNECT)
        parser._process_line(QUALIFYING_CREATED)
        parser._process_line(_new_lap("2026-11-07 23:53:00.547", "01:05.718"))
        parser._process_line(END_SESSION)
        parser._process_line(WARMUP_CREATED)
        parser._process_line(WARMUP_CONNECT)
        parser._process_line(RACE_CREATED)
        parser._process_line(RACE_CONNECT)
        parser._process_line(_new_lap("2026-11-08 00:10:42.461", "01:10.586"))
        parser._process_line(EXIT)

        assert [s.session_type for s in parser.sessions] == [
            "QUALIFYING",
            "RACE",
        ]
        assert parser.sessions[0].laps[0].lap_time_ms == 65718
        assert parser.sessions[1].laps[0].lap_time_ms == 70586
