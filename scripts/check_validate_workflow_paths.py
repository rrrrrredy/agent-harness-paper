from __future__ import annotations

from pathlib import Path


WORKFLOW = Path(".github/workflows/validate.yml")

REQUIRED_PATHS = [
    "README.md",
    "CHANGELOG.md",
    "artifact_manifest.json",
    "benchmark/**",
    "docs/**",
    "evidence/**",
    "experiments/run_manifest.md",
    "harness/**",
    "paper/**",
    "results/**",
    "scripts/**",
    "tests/**",
    ".github/workflows/validate.yml",
]


def main() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    findings: list[str] = []
    for required in REQUIRED_PATHS:
        if f'"{required}"' not in text:
            findings.append(f"missing validation workflow path: {required}")
    if "workflow_dispatch:" not in text:
        findings.append("missing manual workflow_dispatch trigger")
    if findings:
        raise SystemExit("validate workflow path check failed:\n" + "\n".join(findings))
    print("validate workflow path check passed")


if __name__ == "__main__":
    main()
