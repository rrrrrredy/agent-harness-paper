from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from harness.core import evaluate_case, load_cases
from scripts.run_local_reference import reference_actions


def run(command: list[str]) -> str:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return completed.stdout.strip()


def main() -> None:
    print("Agent harness demo walkthrough")
    print("=" * 32)
    print("This walkthrough does not require live model credentials.")
    print()

    cases = load_cases()
    print(f"Loaded {len(cases)} cases from benchmark/cases.jsonl.")

    categories = sorted({case.category for case in cases})
    print("Categories: " + ", ".join(categories))
    print()

    case = next(item for item in cases if item.id == "security_001")
    payload = reference_actions(case, "thin_contract")
    result = evaluate_case(case, payload, provider="local_reference", variant="thin_contract")
    print(f"Sample case: {case.id} ({case.category})")
    print(f"Task: {case.task}")
    print(f"Allowed tools: {', '.join(case.allowed_tools)}")
    print("Reference action payload:")
    print(json.dumps(payload, indent=2))
    print("Evaluation summary:")
    print(
        json.dumps(
            {
                "task_success": result.task_success,
                "state_diff_correct": result.state_diff_correct,
                "permission_violations": result.permission_violations,
                "unsafe_secret_access": result.unsafe_secret_access,
                "replayable": result.replayable,
                "notes": result.notes,
            },
            indent=2,
        )
    )
    print()

    print("Regenerating deterministic reference rows...")
    print(run([sys.executable, "scripts/run_local_reference.py"]))
    print()

    print("Regenerating aggregate tables...")
    print(run([sys.executable, "scripts/analyze_results.py"]))
    print()

    summary = ROOT / "results" / "tables" / "experiment_summary.md"
    print(f"Summary table: {summary}")
    print(summary.read_text(encoding="utf-8").splitlines()[0])
    print(summary.read_text(encoding="utf-8").splitlines()[1])
    for line in summary.read_text(encoding="utf-8").splitlines()[2:8]:
        print(line)


if __name__ == "__main__":
    main()
