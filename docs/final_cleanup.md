# Final Cleanup Checklist

Use this checklist before sharing or submitting the artifact package.

## Required Checks

- `.\.venv\Scripts\python scripts\run_checks.py --mode validate`
- `.\.venv\Scripts\python -m pytest -q`
- `.\.venv\Scripts\python scripts\check_tex_sources.py`
- `.\.venv\Scripts\python scripts\check_public_traces.py`
- `.\.venv\Scripts\python scripts\check_artifact_consistency.py`
- `.\.venv\Scripts\python scripts\secret_scan.py`
- `.\.venv\Scripts\python scripts\audit_source_evidence.py --offline`

## Regeneration Checks

- `.\.venv\Scripts\python scripts\run_checks.py --mode regenerate`
- `.\.venv\Scripts\python scripts\backfill_run_metadata.py`
- `.\.venv\Scripts\python scripts\analyze_results.py`
- `.\.venv\Scripts\python scripts\inspect_failures.py`
- `.\.venv\Scripts\python scripts\generate_figures.py`

## Manual Checks

- Confirm the latest `Build paper PDF` GitHub Actions run succeeds if `paper/` or TeX result tables changed.
- Confirm the checked PDF artifact can be downloaded with `gh run download 28164140135 -n agent-harness-paper-pdf -D logs\artifact-download`.
- Confirm the latest `Validate artifact package` GitHub Actions run succeeds after artifact or script changes.
- Confirm `experiments/run_manifest.md` matches raw result files.
- Confirm manuscript claims remain within `docs/claim_boundaries.md`.
- Confirm live-provider rows are not rerun unless credentials are present in environment variables.
