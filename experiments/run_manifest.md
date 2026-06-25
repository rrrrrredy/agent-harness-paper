# Run Manifest

## Local Reference Run

- Runner: `scripts/run_codex_reference.py`
- Provider label: `codex_reference`
- Purpose: deterministic validation of benchmark mechanics, not model capability.
- Cases: 24
- Variants: `no_harness`, `thick_checklist`, `thin_contract`
- Raw output: `experiments/raw/codex_reference.jsonl`

## DeepSeek Live Run

- Runner: `scripts/run_model_experiment.py --provider deepseek --limit 24`
- Endpoint: `https://api.deepseek.com/chat/completions`
- Model: `deepseek-v4-pro`
- Credential source: process environment variable `DEEPSEEK_API_KEY`
- Cases: 24
- Variants: `no_harness`, `thick_checklist`, `thin_contract`
- Raw output: `experiments/raw/deepseek_live.jsonl`
- Status: completed with 72 raw rows, 24 cases x 3 variants. Aggregate tables were regenerated after completion.
- Metadata: rows include provider, model id, endpoint, schema version, and prompt SHA-256 after `scripts/backfill_run_metadata.py`.

## Kimi Live Attempt

- Runner: `scripts/run_model_experiment.py --provider kimi --variants thin_contract --limit 1`
- Endpoint: `https://api.moonshot.ai/v1/chat/completions`
- Model: `kimi-k2.7-code`
- Credential source: process environment variable `MOONSHOT_API_KEY`
- Raw output: `experiments/raw/kimi_live.jsonl`
- Status: provider returned HTTP 401 invalid authentication for the supplied credential. Treat as provider availability/authentication failure, not model behavior.
- Metadata: row includes provider, model id, endpoint, schema version, and prompt SHA-256 after `scripts/backfill_run_metadata.py`.
