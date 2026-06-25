from __future__ import annotations

import argparse
import subprocess
import sys


VALIDATE = [
    [sys.executable, "-m", "pytest", "-q"],
    [sys.executable, "scripts/check_tex_sources.py"],
    [sys.executable, "scripts/check_public_traces.py"],
    [sys.executable, "scripts/check_artifact_consistency.py"],
    [sys.executable, "scripts/audit_source_evidence.py", "--offline"],
    [sys.executable, "scripts/secret_scan.py"],
]

REGENERATE = [
    [sys.executable, "scripts/backfill_run_metadata.py"],
    [sys.executable, "scripts/analyze_results.py"],
    [sys.executable, "scripts/inspect_failures.py"],
    [sys.executable, "scripts/generate_figures.py"],
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["validate", "regenerate", "all"], default="validate")
    args = parser.parse_args()

    commands = []
    if args.mode in {"regenerate", "all"}:
        commands.extend(REGENERATE)
    if args.mode in {"validate", "all"}:
        commands.extend(VALIDATE)
    for command in commands:
        print("+ " + " ".join(command), flush=True)
        subprocess.run(command, check=True)


if __name__ == "__main__":
    main()
