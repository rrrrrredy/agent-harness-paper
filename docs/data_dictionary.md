# Data Dictionary

This document defines the committed benchmark, raw-result, derived-result, and validation artifact fields used by the paper package.

## Benchmark Cases

Source: `benchmark/cases.jsonl`

Each row is one task case.

- `id`: Stable case identifier, such as `trigger_001`.
- `category`: Case family. Values are `trigger_routing`, `stateful_tool_use`, `permission_security`, `memory_scoping`, and `replay_recovery`.
- `task`: User-facing task instruction given to the runner.
- `initial_state`: Simulated world state before the action plan is evaluated.
- `initial_state.files`: File-system-like map from path to content.
- `allowed_tools`: Tools permitted for the case.
- `expected.should_act`: Whether the agent should act rather than refuse or defer.
- `expected.required_tools`: Tool names that must appear for success.
- `expected.forbidden_tools`: Tool names that must not appear.
- `expected.target_path`: Optional file path or object expected to be read or changed.
- `expected.state_assertions`: Optional state checks evaluated after tool simulation.

## Raw Result Rows

Sources: `experiments/raw/*.jsonl`

Each row is one provider, prompt variant, and case result.

- `case_id`: Case identifier from `benchmark/cases.jsonl`.
- `category`: Copied case category.
- `provider`: Runner/provider label, such as `codex_reference`, `deepseek`, or `kimi`.
- `variant`: Prompt variant. Values are `no_harness`, `thick_checklist`, and `thin_contract`.
- `task_success`: Boolean task-level success under harness scoring.
- `state_diff_correct`: Boolean final-state assertion result.
- `invalid_tool_calls`: Count of tool names or argument shapes not accepted by the harness.
- `permission_violations`: Count of forbidden or disallowed side-effect attempts.
- `unsafe_secret_access`: Count of unsafe secret-read attempts.
- `over_under_trigger_error`: Count-like routing error flag for refusing required work or acting outside scope.
- `replayable`: Whether the result includes enough structured action/state information for replay.
- `recovered`: Whether the runner recovered from the injected or expected failure condition.
- `actions`: Parsed tool-action list, when available.
- `final_state`: Simulated post-run state after applying parsed actions.
- `notes`: Human-readable evaluator notes and provider/parser failure labels.
- `usage`: Provider metadata for live rows.
- `raw_response`: Raw model response text for live rows, when recorded.

## Live Usage Metadata

Required for `deepseek_live.jsonl` and `kimi_live.jsonl` after metadata backfill.

- `provider`: Provider key used by the runner.
- `model`: Model identifier configured in `harness/providers.py`.
- `endpoint`: Chat completion endpoint used by the runner.
- `schema_version`: Artifact schema label. Current value: `agent-harness-paper/v1`.
- `prompt_sha256`: SHA-256 hash of the exact prompt built for the case and variant.
- `prompt_tokens`, `completion_tokens`, `total_tokens`: Provider token counts when returned.
- `elapsed_seconds`: Wall-clock request time when recorded.
- `usage.rerun_reason`: Optional repair reason. Current committed DeepSeek repair rows use `parse_error`.

## Derived Tables

Sources: `results/tables/*.md`, `results/tables/*.csv`, and `results/tables/*.tex`

### Experiment Summary

- `provider`: Provider label.
- `variant`: Prompt variant.
- `n_total`: Total raw rows.
- `n_executed`: Rows excluding provider availability/authentication errors.
- `provider_errors`: Provider availability/authentication error count.
- `parse_errors`: JSON or action-plan parse failure count.
- `task_success_rate`: Mean `task_success` over executed rows.
- `state_diff_rate`: Mean `state_diff_correct` over executed rows.
- `permission_violations`: Sum over executed rows.
- `invalid_tool_calls`: Sum over executed rows.
- `unsafe_secret_access`: Sum over executed rows.
- `routing_errors`: Sum of `over_under_trigger_error` over executed rows.
- `recovery_rate`: Mean `recovered` over executed rows.

### Category Summary

- `provider`: Provider label.
- `variant`: Prompt variant.
- `category`: Case family.
- `n_total`: Raw rows in the group.
- `n_executed`: Rows excluding provider availability/authentication errors.
- `success_rate`: Mean `task_success` over executed rows.
- `state_diff_rate`: Mean `state_diff_correct` over executed rows.
- `routing_errors`: Sum of `over_under_trigger_error`.

### Failure Taxonomy

- `provider`: Provider label.
- `variant`: Prompt variant.
- `failure_class`: One of `provider_error`, `parse_error`, `invalid_tool_call`, `permission_violation`, `unsafe_secret_access`, `routing_error`, `state_diff_error`, or `other_behavior_failure`.
- `count`: Number of rows assigned to the class.

## Validation Artifacts

- `scripts/run_checks.py --mode validate`: Deterministic validation entrypoint.
- `scripts/run_checks.py --mode regenerate`: Derived-result regeneration entrypoint.
- `scripts/check_run_manifest_alignment.py`: Checks raw-result counts, live metadata, parse-error counts, and provider-error status against `experiments/run_manifest.md`.
- `scripts/check_release_references.py`: Checks checked PDF artifact references and prevents moving validation run IDs from being committed.
- `scripts/build_artifact_archive.py --check`: Checks archive file selection without writing a zip.
- `scripts/check_provider_credentials.py`: Checks provider credential environment-variable presence before live reruns without printing credential values.
- `scripts/run_model_experiment.py --output`: Writes live rerun rows to a selected JSONL path and refuses accidental overwrite unless `--resume` or `--force-overwrite` is supplied.
- `.github/workflows/validate.yml`: Remote validation workflow.
- `.github/workflows/latex.yml`: Remote PDF build workflow.
