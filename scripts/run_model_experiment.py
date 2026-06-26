from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness.core import evaluate_case, load_cases
from harness.prompts import VARIANTS, build_prompt
from harness.providers import PROVIDERS, call_provider, require_provider_key


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", choices=["deepseek", "kimi"], required=True)
    parser.add_argument("--variants", nargs="+", choices=VARIANTS, default=list(VARIANTS))
    parser.add_argument("--limit", type=int, default=24)
    parser.add_argument("--output", help="Output JSONL path. Defaults to experiments/raw/{provider}_live.jsonl.")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--force-overwrite", action="store_true")
    args = parser.parse_args()
    try:
        require_provider_key(args.provider)
    except RuntimeError as exc:
        raise SystemExit(str(exc)) from exc

    cases = load_cases()[: args.limit]
    out = resolve_output_path(args.provider, args.output)
    validate_output_mode(out, resume=args.resume, force_overwrite=args.force_overwrite)
    out.parent.mkdir(parents=True, exist_ok=True)
    completed = set()
    if args.resume and out.exists():
        for line in out.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                completed.add((row["case_id"], row["variant"]))
    mode = "a" if args.resume else "w"
    with out.open(mode, encoding="utf-8") as handle:
        for case in cases:
            for variant in args.variants:
                if (case.id, variant) in completed:
                    continue
                try:
                    prompt = build_prompt(case, variant)
                    model_result = call_provider(args.provider, prompt)
                    model_result["usage"] = model_result["usage"] | {
                        "model": PROVIDERS[args.provider]["model"],
                        "endpoint": PROVIDERS[args.provider]["base_url"],
                        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
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
                except Exception as exc:
                    result = evaluate_case(
                        case,
                        {"actions": []},
                        provider=args.provider,
                        variant=variant,
                        raw_response=f"ERROR: {exc}",
                    )
                    result.notes.append(f"provider_error:{exc}")
                handle.write(json.dumps(result.to_dict(), ensure_ascii=False) + "\n")
                handle.flush()
                print(f"{args.provider} {variant} {case.id}: success={result.task_success}", flush=True)
    print(f"wrote {out}")


def resolve_output_path(provider: str, output: str | None) -> Path:
    if output:
        return Path(output)
    return Path(f"experiments/raw/{provider}_live.jsonl")


def validate_output_mode(path: Path, *, resume: bool, force_overwrite: bool) -> None:
    if path.exists() and not resume and not force_overwrite:
        raise SystemExit(
            f"output exists: {path}. Use --resume, --force-overwrite, or --output logs/live-reruns/<file>.jsonl"
        )


if __name__ == "__main__":
    main()
