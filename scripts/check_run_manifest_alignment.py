from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any


RAW = Path("experiments/raw")
RUN_MANIFEST = Path("experiments/run_manifest.md")


EXPECTED_COUNTS = {
    "codex_reference.jsonl": 72,
    "deepseek_live.jsonl": 72,
    "kimi_live.jsonl": 1,
}

EXPECTED_VARIANTS = {
    ("codex_reference", "no_harness"): 24,
    ("codex_reference", "thick_checklist"): 24,
    ("codex_reference", "thin_contract"): 24,
    ("deepseek", "no_harness"): 24,
    ("deepseek", "thick_checklist"): 24,
    ("deepseek", "thin_contract"): 24,
    ("kimi", "thin_contract"): 1,
}

LIVE_USAGE_FIELDS = ["provider", "model", "endpoint", "schema_version", "prompt_sha256"]


def main() -> None:
    findings: list[str] = []
    rows_by_file = {path.name: _load_jsonl(path) for path in RAW.glob("*.jsonl")}

    for name, expected in EXPECTED_COUNTS.items():
        actual = len(rows_by_file.get(name, []))
        if actual != expected:
            findings.append(f"{name}: expected {expected} rows, found {actual}")

    distribution = Counter((row.get("provider"), row.get("variant")) for rows in rows_by_file.values() for row in rows)
    for key, expected in EXPECTED_VARIANTS.items():
        actual = distribution.get(key, 0)
        if actual != expected:
            findings.append(f"{key}: expected {expected} rows, found {actual}")

    for name in ["deepseek_live.jsonl", "kimi_live.jsonl"]:
        for index, row in enumerate(rows_by_file.get(name, []), start=1):
            usage = row.get("usage") or {}
            for field in LIVE_USAGE_FIELDS:
                if field not in usage:
                    findings.append(f"{name}:{index}: missing usage.{field}")

    deepseek_rows = rows_by_file.get("deepseek_live.jsonl", [])
    deepseek_parse_errors = sum(_has_note(row, "parse_error:") for row in deepseek_rows)
    deepseek_rerun_rows = sum((row.get("usage") or {}).get("rerun_reason") == "parse_error" for row in deepseek_rows)
    if deepseek_parse_errors != 2:
        findings.append(f"deepseek_live.jsonl: expected 2 parse-error rows, found {deepseek_parse_errors}")
    if deepseek_rerun_rows != 3:
        findings.append(f"deepseek_live.jsonl: expected 3 usage.rerun_reason=parse_error rows, found {deepseek_rerun_rows}")

    kimi_provider_errors = sum(_has_note(row, "provider_error:") for row in rows_by_file.get("kimi_live.jsonl", []))
    if kimi_provider_errors != 1:
        findings.append(f"kimi_live.jsonl: expected 1 provider-error row, found {kimi_provider_errors}")

    manifest = RUN_MANIFEST.read_text(encoding="utf-8")
    required_manifest_phrases = [
        "completed with 72 raw rows",
        "usage.rerun_reason=parse_error",
        "Current aggregate tables count 2 parse-error rows",
        "provider returned HTTP 401 invalid authentication",
    ]
    for phrase in required_manifest_phrases:
        if phrase not in manifest:
            findings.append(f"{RUN_MANIFEST}: missing phrase: {phrase}")

    if findings:
        raise SystemExit("run manifest alignment check failed:\n" + "\n".join(findings))
    print("run manifest alignment check passed")


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _has_note(row: dict[str, Any], prefix: str) -> bool:
    return any(str(note).startswith(prefix) for note in row.get("notes", []))


if __name__ == "__main__":
    main()
