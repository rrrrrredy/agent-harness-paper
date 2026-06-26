from __future__ import annotations

from pathlib import Path


REGISTER = Path("docs/external_decision_register.md")

REQUIRED_DECISIONS = [
    "venue template",
    "license",
    "anonymization policy",
    "artifact sharing mode",
    "live-provider rerun policy",
]

REQUIRED_TERMS = [
    "external decision required",
    "safe default",
    "unblock action",
    "submission gate",
]


def main() -> None:
    if not REGISTER.exists():
        raise SystemExit(f"missing external decision register: {REGISTER}")

    text = REGISTER.read_text(encoding="utf-8").lower()
    findings: list[str] = []
    for decision in REQUIRED_DECISIONS:
        if decision not in text:
            findings.append(f"missing decision row: {decision}")
    for term in REQUIRED_TERMS:
        if term not in text:
            findings.append(f"missing required register term: {term}")
    if "sk-" in text:
        findings.append("external decision register must not contain credential-looking values")
    if findings:
        raise SystemExit("external decision register check failed:\n" + "\n".join(findings))
    print("external decision register check passed")


if __name__ == "__main__":
    main()
