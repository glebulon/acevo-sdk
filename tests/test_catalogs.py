from acevo.catalogs import find_track_by_name, select_track_profile


def test_find_track_by_name_matches_alias() -> None:
    key, profile = find_track_by_name("Brands Hatch")

    assert key
    assert profile["display_name"]


def test_select_track_profile_handles_missing_track() -> None:
    key, profile = select_track_profile("definitely-not-a-track")

    assert key is None
    assert profile is None
