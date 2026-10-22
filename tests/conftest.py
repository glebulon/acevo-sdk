"""Shared pytest fixtures and helpers for acevo-sdk tests."""

import pytest

from acevo import LapData, LogParser, SessionData
from acevo._logging import Component, log_debug


def make_parser(car_id: str, with_completed_lap: bool = False) -> LogParser:
    """Create a LogParser initialized with the given car UUID for testing."""
    parser = LogParser()
    parser.context.car_uuid = car_id
    parser.context.player_car_uuids.add(car_id)
    parser.current_session = SessionData(car_uuid=car_id)
    if with_completed_lap:
        parser.current_session.laps.append(
            LapData(
                lap_number=1,
                physics_lap_number=1,
                lap_time_ms=100000,
                lap_time_str="1:40.000",
            )
        )
    return parser


@pytest.fixture(scope="session", autouse=True)
def _warm_up_logger():
    """Pay the one-time logger setup cost before tests run."""
    log_debug(Component.LOG_PARSER, "[conftest] logger warm-up")
