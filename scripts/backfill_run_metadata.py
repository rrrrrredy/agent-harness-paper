from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness.core import load_cases
from harness.prompts import build_prompt
from harness.providers import PROVIDERS


RAW_FILES = {
    "deepseek": Path("experiments/raw/deepseek_live.jsonl"),
    "kimi": Path("experiments/raw/kimi_live.jsonl"),
}


def main() -> None:
    cases = {case.id: case for case in load_cases()}
    changed = 0
    for provider, path in RAW_FILES.items():
        if not path.exists():
            continue
        rows = []
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            row, did_change = _backfill_row(provider, row, cases)
            rows.append(row)
            changed += int(did_change)
        path.write_text(
            "\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n",
            encoding="utf-8",
        )
    print(f"backfilled metadata in {changed} rows")


def _backfill_row(provider: str, row: dict[str, Any], cases: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    usage = dict(row.get("usage") or {})
    before = json.dumps(usage, sort_keys=True)
    config = PROVIDERS[provider]
    usage.setdefault("model", config["model"])
    usage.setdefault("endpoint", config["base_url"])
    usage.setdefault("provider", provider)
    usage.setdefault("schema_version", "agent-harness-paper/v1")
    case = cases.get(row.get("case_id"))
    variant = row.get("variant")
    if case is not None and isinstance(variant, str):
        prompt = build_prompt(case, variant)
        usage.setdefault("prompt_sha256", hashlib.sha256(prompt.encode("utf-8")).hexdigest())
    row["usage"] = usage
    after = json.dumps(usage, sort_keys=True)
    return row, before != after


if __name__ == "__main__":
    main()
