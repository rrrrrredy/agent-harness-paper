# Run Manifest

## Local Reference Run

- Runner: `scripts/run_local_reference.py`
- Provider label: `local_reference`
- Purpose: deterministic validation of benchmark mechanics, not model capability.
- Cases: 24
- Variants: `no_harness`, `thick_checklist`, `thin_contract`
- Raw output: `experiments/raw/local_reference.jsonl`

## DeepSeek Live Run

- Runner: `scripts/run_model_experiment.py --provider deepseek --limit 24`
- Endpoint: `https://api.deepseek.com/chat/completions`
- Model: `deepseek-v4-pro`
- Credential source: process environment variable `DEEPSEEK_API_KEY`
- Cases: 24
- Variants: `no_harness`, `thick_checklist`, `thin_contract`
- Raw output: `experiments/raw/deepseek_live.jsonl`
- Status: refreshed on 2026-06-26 from reviewed `logs/live-reruns/deepseek_full_smoke.jsonl`, then promoted into committed raw results with 72 raw rows, 24 cases x 3 variants. Aggregate tables were regenerated after promotion.
- Metadata: rows include provider, model id, endpoint, schema version, and prompt SHA-256 directly from `scripts/run_model_experiment.py`.
- Parse-error status: current aggregate tables count 1 parse-error row. No current DeepSeek rows carry `usage.rerun_reason=parse_error`.

## Kimi Live Run

- Runner: `scripts/run_model_experiment.py --provider kimi --limit 24`
- Endpoint: `https://api.moonshot.cn/v1/chat/completions`
- Model: `kimi-k2.7-code`
- Credential source: process environment variable `MOONSHOT_API_KEY`
- Cases: 24
- Variants: `no_harness`, `thick_checklist`, `thin_contract`
- Raw output: `experiments/raw/kimi_live.jsonl`
- Status: refreshed on 2026-06-26 from reviewed `logs/live-reruns/kimi_full_smoke.jsonl`, then promoted into committed raw results with 72 raw rows, 24 cases x 3 variants. Aggregate tables were regenerated after promotion.
- Metadata: rows include provider, model id, endpoint, schema version, prompt SHA-256, token counts, and elapsed seconds directly from `scripts/run_model_experiment.py`.
- Parse-error status: current aggregate tables count 2 Kimi parse-error rows. No current Kimi rows are provider-error rows.
