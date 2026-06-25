from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness.core import evaluate_case, load_cases
from harness.prompts import build_prompt
from harness.providers import PROVIDERS, call_provider


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=["deepseek", "kimi"], required=True)
    args = parser.parse_args()

    path = Path(f"experiments/raw/{args.provider}_live.jsonl")
    if not path.exists():
        raise SystemExit(f"missing {path}")
    cases = {case.id: case for case in load_cases()}
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    changed = 0
    for index, row in enumerate(rows):
        notes = [str(note) for note in row.get("notes", [])]
        if not any(note.startswith("provider_error:Expecting") or note.startswith("parse_error:") for note in notes):
            continue
        case = cases[row["case_id"]]
        variant = row["variant"]
        prompt = build_prompt(case, variant)
        model_result = call_provider(args.provider, prompt)
        model_result["usage"] = model_result["usage"] | {
            "model": PROVIDERS[args.provider]["model"],
            "endpoint": PROVIDERS[args.provider]["base_url"],
            "provider": args.provider,
            "schema_version": "agent-harness-paper/v1",
            "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
            "rerun_reason": "parse_error",
        }
        result = evaluate_case(
            case,
            model_result["payload"],
            provider=args.provider,
            variant=variant,
            usage=model_result["usage"],
            raw_response=model_result["raw_response"],
        )
        if "_parse_error" in model_result["payload"]:
            result.notes.append(f"parse_error:{model_result['payload']['_parse_error']}")
        rows[index] = result.to_dict()
        changed += 1
        print(f"reran {args.provider} {variant} {case.id}: success={result.task_success}", flush=True)
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")
    print(f"updated {changed} rows in {path}")


if __name__ == "__main__":
    main()
