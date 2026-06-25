from __future__ import annotations

from pathlib import Path


REQUIRED_COMMANDS = [
    "run_checks.py --mode validate",
    "run_checks.py --mode regenerate",
]

ENTRYPOINTS = [
    Path("README.md"),
    Path("artifact_manifest.json"),
    Path("docs/artifact_release_index.md"),
    Path("docs/final_cleanup.md"),
    Path("docs/reproducibility.md"),
    Path("docs/reviewer_guide.md"),
]


def main() -> None:
    findings: list[str] = []
    for path in ENTRYPOINTS:
        text = path.read_text(encoding="utf-8", errors="ignore")
        for command in REQUIRED_COMMANDS:
            if command not in text:
                findings.append(f"{path}: missing {command}")
    if findings:
        raise SystemExit("entrypoint command check failed:\n" + "\n".join(findings))
    print("entrypoint command check passed")


if __name__ == "__main__":
    main()
