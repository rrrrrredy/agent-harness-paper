# Changelog

## Current Artifact Package

- Created the LaTeX manuscript and supporting bibliography.
- Added a 24-case replayable benchmark for routing, stateful tool use, permission/security, memory scoping, and replay/recovery.
- Added deterministic reference results, live DeepSeek results, and a recorded Kimi authentication-failure attempt.
- Added regenerated aggregate tables, category summaries, failure taxonomy, failure inspection, and SVG figure.
- Added GitHub metadata snapshots, path-level source evidence audit, and explicit claim-boundary documentation.
- Added claim-to-evidence traceability and validation for manuscript claim boundaries.
- Added an external decision register for venue, license, anonymization, artifact-sharing, and live-rerun decisions.
- Added live-rerun promotion guidance and overwrite protection for provider smoke outputs.
- Added archive packaging, archive-manifest alignment checks, and clean-room archive smoke audits.
- Renamed the deterministic reference run to `local_reference` to keep reviewer-facing artifacts provider-neutral.
- Fixed provider-error classification so the Kimi authentication failure is not counted as model behavior.
- Added an independent verification pass and regression coverage for provider-error classification.
- Added GitHub Actions PDF build workflow and verified successful PDF artifact generation.
- Refreshed the checked PDF artifact reference to run `28212313090`.
- Added reviewer handoff files: `artifact_manifest.json` and `docs/reviewer_guide.md`.
- Added offline validation for the source evidence audit.

## Remaining Optional Work

- Rerun live provider rows only when valid provider keys are present in environment variables.
- Perform deeper source-code audits before making stronger implementation-behavior claims.
- Adapt the manuscript to a target venue format if a venue is selected.
