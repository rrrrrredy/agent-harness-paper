from __future__ import annotations

from pathlib import Path


TRACEABILITY = Path("docs/claim_traceability.md")

REQUIRED_REFERENCES = [
    "docs/claim_boundaries.md",
    "evidence/github_snapshots.md",
    "evidence/source_audit.md",
    "benchmark/cases.jsonl",
    "experiments/raw/*.jsonl",
    "experiments/run_manifest.md",
    "docs/live_rerun_promotion.md",
    "artifact_manifest.json",
]

REQUIRED_BOUNDARIES = [
    "not a deployed-production proof",
    "not full runtime behavior",
    "not representative of all agent tasks",
    "No general model/provider superiority claim",
    "Venue template, license, anonymization, and live rerun decisions remain external",
]


def main() -> None:
    text = TRACEABILITY.read_text(encoding="utf-8")
    findings = []
    for item in REQUIRED_REFERENCES:
        if item not in text:
            findings.append(f"missing reference: {item}")
    for item in REQUIRED_BOUNDARIES:
        if item not in text:
            findings.append(f"missing boundary: {item}")
    if findings:
        raise SystemExit("claim traceability check failed:\n" + "\n".join(findings))
    print("claim traceability check passed")


if __name__ == "__main__":
    main()
