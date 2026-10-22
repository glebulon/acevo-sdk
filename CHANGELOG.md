# Changelog

## 0.2.0

- Synced with sim-laps-client @ HEAD (post-split development through Oct 2026).
- Log parser: ACE v0.7 log-format support, log-authoritative lap detection,
  cooperative async line iteration, session restart/boundary handling,
  penalty dedup, offline single-player and multiplayer support.
- Shared session: `LapCompletionData` live SHM completions,
  `SubmissionFallbackSnapshot`, terminal/replay state detection,
  hybrid-flag tracking.
- Capture: `record_frames` validity-only mode, `CaptureSnapshot`,
  `LapBoundary` binding/reconciliation, `configure()`,
  `game_running_callback` injection.
- Decoder: `peek_graphics_validity` lightweight SHM peek, graphics decode
  sanity checks, static-payload sanitization; dropped legacy ACC fields.
- Catalogs: `resolve_track_key`/`track_slug`, expanded bundled track data,
  new car tuning catalog (`get_tuning_params`, `format_tuning_block`).
- Models: `LapState.PUSH` renamed to `LapState.VALID` (breaking);
  `LapData.validity_source` and `LapData.result_id` added;
  `is_hybrid_car()` replaces hardcoded hybrid-car list.
- Ported the upstream regression test suite (~640 tests).

## 0.1.0

- Initial Alpha release.
- Added ACE log parser.
- Added Windows shared-memory capture.
- Added shared-memory decoders for physics, graphics, and static regions.
- Added reusable lap/session/capture models and shared session state.
- Added bundled track catalog helpers.
