from __future__ import annotations

import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from harness.core import Case, evaluate_case, load_cases
from harness.prompts import VARIANTS


OUT = Path("experiments/raw/codex_reference.jsonl")


def reference_actions(case: Case, variant: str) -> dict:
    required = case.expected.get("required_tools", [])
    actions = []
    for tool in required:
        args = {}
        if tool in {"read_file", "write_file"}:
            args["path"] = case.expected.get("target_path", "README.md")
        if tool == "write_file":
            args["content"] = case.expected.get("write_content", "updated by harness")
        if tool == "forget_memory":
            args["key"] = case.expected.get("memory_key", "stale_project")
        if tool in {"create_report_candidate", "request_review"}:
            args["id"] = case.expected.get("report_id", "candidate")
            args["content"] = case.expected.get("report_content", "candidate with citations and caveats")
        actions.append({"tool": tool, "args": args})
    if not actions and not case.expected.get("should_act", True):
        actions = []
    return {"actions": actions, "final": "reference trajectory"}


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    cases = load_cases()
    with OUT.open("w", encoding="utf-8") as handle:
        for case in cases:
            for variant in VARIANTS:
                payload = reference_actions(case, variant)
                result = evaluate_case(case, payload, provider="codex_reference", variant=variant)
                handle.write(json.dumps(result.to_dict(), ensure_ascii=False) + "\n")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
