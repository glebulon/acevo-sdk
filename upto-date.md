# acevo-sdk up-to-date tracker

Baseline: SDK = sim-laps-client @ `6e2aca8` (2026-05-26). Gap: ~73 commits,
+3510/−1750 lines across the extraction modules.

Approach: upstream HEAD files were ported wholesale (the original extraction was
mechanical), then re-adapted to SDK import layout + py310 `X | None` style.
Verified by normalized diff vs upstream HEAD — remaining diffs are only the
intentional SDK adaptations listed under "Notes / decisions".

## Port checklist

### 1. LogParser — ACE v0.7 log-format update (`2b9d496`)
- [x] `connect` regex: `connected(?: \([^)]+\))?` (was `\(\d+\)`)
- [x] `lap_validity` regex captures `flags` group
- [x] `_last_setup_car_uuid` / `_pending_compound_source_car_uuid` — compound batching scoped to source car
- [x] LOADING fallback guard: don't overwrite a resolved compound
- [x] Same-timestamp flush when all 4 positions pending

### 2. LogParser — log-authoritative lap detection (`772bc4e`, `d199efe`, validity fixes)
- [x] `_parse_authoritative_lap_validity` (Relevant onSplit)
- [x] `_take_ready_shm_lap` / `_flush_pending_lap_after_grace` / `_apply_shm_fallback_validity`
- [x] `_nearest_lap_match`, `_get_shm_hybrid_flags`, `_line_ts_epoch_seconds`
- [x] Publish laps when ACE omits validity broadcasts (`cc052d4`)
- [x] Keep historical laps silent at session exit (`aebbb52`)
- [x] onSplit format hardening (`b10a871`)
- [x] Don't drop lap if quit after crossing line (`20de6ee`)
- [x] Penalty dedup — `_handle_penalty_signals` (`3584c2b`)
- [x] Parser bug fixes (`f8feab5`)

### 3. LogParser — async + structure refactor
- [x] `_iter_lines_cooperatively` — yield while parsing large logs (`ac2cc04`)
- [x] Log-tail maintenance for partial lines (`9c4a699`)
- [x] `_preprocess_line` + `_process_*` split of `_process_line`
- [x] `_emit_lap_update` / `_emit_session_restart` / `_emit_user_detected` callbacks
- [x] `_restart_session_in_place`, `_reset_session_boundary`, `_maybe_boundary_for_identity_change`
- [x] `_normalize_track_key`, `_session_has_content`, `_handle_player_car_binding`
- [x] `_maybe_start_fallback_session` — nord practice / tourist fixes (`d1719fd`, `6c7cc1b`, `cd49f83`)

### 4. LogParser — multiplayer + cross-session
- [x] Multiplayer telemetry log parsing (`059309a`)
- [x] Cross-session lap-time contamination fixes (`af83254`, `9e11973`)

### 5. SharedSessionManager
- [x] `LapCompletionData` + consume/query APIs (`get_latest_lap_completion`, `get_lap_completions_after`, `get_lap_completion_by_time`, `consume_lap_completion`)
- [x] `SubmissionFallbackSnapshot` + `get_submission_fallbacks`
- [x] Graphics-state classification (`_is_terminal_graphics_state`, `_is_replay_graphics_state`, `_is_non_live_session_phase`)
- [x] `has_live_timer_ownership`, `get_hybrid_flags`
- [x] `update_lap_timing_from_graphics_shm`, `update_session_metadata_from_logs`, `update_from_telemetry`
- [x] Report identity/ownership fixes (atomic recorder ownership, verdict resets, live-timer ownership for SHM completions)

### 6. TelemetryCapture
- [x] `record_frames` validity-only mode + `set_record_frames` (`3e97bf1`)
- [x] `CaptureSnapshot` / `LapBoundary` + `bind_lap_boundary` / `reconcile_lap_boundary` / `get_lap_boundaries`
- [x] Stop snapshots: `set_on_stop_snapshot_callback`, `get_last_stop_snapshot`, `_freeze_stop_snapshot`, `set_source_context`
- [x] `_start_recording_at_timing_boundary`
- [x] Keep-alive while stationary (`7a5de2f`), injectable backend (`111c0d6`), `configure()`
- [x] `is_game_running()` → `game_running_callback` injection (SDK keeps no game-process detection)

### 7. Decoder
- [x] `peek_graphics_validity` — lightweight SHM validity peek (`4a5e74d`)
- [x] `_sanity_check_graphics_evo` + `decode_static()` sanitization + shared SHM size constants (`751128a`)
- [x] Timing keys: `timing_delta_current_p`, `timing_delta_last_p`, `timing_last_laptime`; field-name fix (`ae53525`)
- [x] Drop ~90 dead legacy ACC keys

### 8. Catalogs
- [x] `resolve_track_key` / `track_slug` / `_corner_confidence` in tracks.py
- [x] Exact layout-name resolution (`76224a3`, `b4c2481`), Nordschleife variants (`5f2f0d1`), name fixes (`d0e2393`)
- [x] Refresh bundled `track_catalog.json` (58KB → 111KB)
- [x] Add `catalogs/cars.py` + `car_tuning_catalog.json` (~95KB) — included; standalone data module, no scripts ported

### 9. Models
- [x] `LapState.PUSH` → `VALID` (breaking; noted in CHANGELOG/README)
- [x] `LapData.validity_source` + `LapData.result_id`
- [x] `InProgressLap` — dropped accumulated validity flags
- [x] `is_hybrid_car()` from SHM flags replaces `KNOWN_HYBRID_CARS` + fuel-spike thresholds
- [x] `LAP_TIME_RECONCILIATION_TOLERANCE_MS` constant

### 10. Tests / housekeeping
- [x] Ported upstream regression tests (651 passing): all 12 `test_log_parser_*`,
  `test_shared_session`, `test_telemetry_decoder_comprehensive`,
  `test_telemetry_capture`, `test_telemetry_capture_advanced`,
  `test_telemetry_capture_coverage`, `test_track_catalog`,
  `test_car_tuning_catalog`, `test_tyre_state_model` + existing SDK tests
- [x] Version sync: `__init__.py` + `pyproject.toml` → 0.2.0
- [x] `Component.SHARED_SESSION` added to `_logging.py`
- [x] CHANGELOG + README updated

## Skipped upstream tests (documented, not ported)

- `test_telemetry_decoder_real_data.py`, `test_captured_fixture_regressions.py`
  — need `tests/fixtures/sample_telemetry.jsonl` (28MB) / analyzer pipeline
- `test_telemetry_integrity_regressions.py`, `test_outlap_public_flow.py`
  — exercise `telemetry_analyzer` + `html_renderer` + UI (out of SDK scope)
- `test_capture_lifecycle_regression.py` — exercises
  `TelemetryLifecycleService` (UI-layer ownership), not the SDK capture
- `test_multiplayer_results.py`, UI/service tests — UI scope

## Notes / decisions

- SDK replaces `is_game_running()`/`GameProcessStatus` with the injectable
  `game_running_callback` (README already documented this contract).
- `get_default_output_dir()` stays ACEVO-branded (`~/Documents/ACEVO/Telemetry`).
- Test adaptation: `patch("...is_game_running")` →
  `patch.object(capture, "_game_running_callback", ...)`; the one test using
  `TelemetryLifecycleService.handle_auto_stop` inlines the equivalent
  `analyzer.analyze(...)` snapshot call.
- `LapState.VALID` is a breaking rename vs 0.1.x `PUSH` — accepted per
  alpha-status README note; version bumped to 0.2.0.
- Car tuning catalog ported as data+helpers only; upstream
  `scripts/update_catalog.py`/`validate_catalog.py` not ported (release tooling).
- Lint: `ruff check .` clean; `pytest`: 651 passed.

## Post-sync fix: coarse monotonic clocks (Windows CI py3.10-3.12)

- `LapCompletionData.observed_at` = `time.monotonic()`, which on Windows
  Python <3.13 uses `GetTickCount64` (~15.6 ms ticks). Two completions in the
  same tick shared `observed_at`, so `consumed_lap_completion_times` (a set
  keyed on it) and the parser's `> observed_at` cursor collapsed them,
  silently dropping the second lap.
- Fix (two parts, applied to both repos):
  1. `SharedSessionManager.update_from_graphics_shm`: nudge `observed_at`
     to `last + 1e-6` when monotonic doesn't advance, keeping it strictly
     increasing per queue.
  2. `LogParser._take_ready_shm_lap`: clamp the grace-check elapsed time
     to `>= 0` — a nudged `observed_at` sits ~1us in the future while the
     tick is frozen, and an unclamped negative diff would defer the
     completion until the clock next ticks.
  Verified under a fully simulated frozen clock; 651 tests pass, ruff
  clean. Same patch applied to sim-laps-client to keep the files in sync.
- CI note (warnings only): `actions/checkout@v4`/`actions/setup-python@v5`
  Node 20 deprecation; `ubuntu-latest` migrating to Ubuntu 26 (Oct 2026).
