# Live Rerun Promotion Checklist

This checklist governs how a new provider smoke run under `logs/live-reruns/` can become a cited raw result under `experiments/raw/`.

## Smoke Run

1. Run provider credential preflight:

   ```powershell
   python scripts\check_provider_credentials.py --provider deepseek
   python scripts\check_provider_credentials.py --provider kimi
   ```

2. Write smoke output to ignored local storage:

   ```powershell
   python scripts\run_model_experiment.py --provider deepseek --variants thin_contract --output logs\live-reruns\deepseek_live.jsonl
   python scripts\run_model_experiment.py --provider kimi --variants thin_contract --output logs\live-reruns\kimi_live.jsonl
   ```

3. Inspect row count, provider labels, variants, notes, usage metadata, and raw response preservation before promotion.

## Promotion Criteria

- Credential values were never committed, printed into docs, or stored in raw rows.
- Smoke rows have expected `provider`, `variant`, `case_id`, and `category` fields.
- Live rows include `usage.model`, `usage.endpoint`, `usage.provider`, `usage.schema_version`, and `usage.prompt_sha256` after metadata backfill.
- Provider availability failures remain labeled as `provider_error`.
- Parser failures remain labeled as `parse_error`.
- The run is intentionally chosen to replace or extend the committed raw-result base.
- `experiments/run_manifest.md` is updated to describe what changed.
- Result tables and figures are regenerated.
- Manuscript claims remain within `docs/claim_boundaries.md`.

## Promotion Sequence

1. Copy the reviewed smoke JSONL into the intended `experiments/raw/` path.
2. If replacing an existing committed raw file through the runner, use `--force-overwrite` explicitly.
3. Run `python scripts\backfill_run_metadata.py`.
4. Run `python scripts\analyze_results.py`.
5. Run `python scripts\inspect_failures.py`.
6. Run `python scripts\generate_figures.py`.
7. Update `experiments/run_manifest.md`, `docs/experiment_protocol.md`, and manuscript result wording if metrics changed.
8. Run `python scripts\run_checks.py --mode all`.
9. Build or refresh the PDF workflow artifact if `paper/` or TeX tables changed.
10. Update checked PDF references if the PDF artifact run changes.
