from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys


def maybe_reexec_project_venv() -> None:
    root = Path(__file__).resolve().parents[1]
    candidates = [
        root / ".venv" / "Scripts" / "python.exe",
        root / ".venv" / "bin" / "python",
    ]
    current = Path(sys.executable).resolve()
    for candidate in candidates:
        if candidate.exists() and candidate.resolve() != current:
            os.execv(str(candidate), [str(candidate), *sys.argv])


maybe_reexec_project_venv()


VALIDATE = [
    [sys.executable, "-m", "pytest", "-q"],
    [sys.executable, "scripts/check_tex_sources.py"],
    [sys.executable, "scripts/check_public_traces.py"],
    [sys.executable, "scripts/check_artifact_consistency.py"],
    [sys.executable, "scripts/check_entrypoint_commands.py"],
    [sys.executable, "scripts/check_release_references.py"],
    [sys.executable, "scripts/check_status_notes.py"],
    [sys.executable, "scripts/check_run_manifest_alignment.py"],
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
