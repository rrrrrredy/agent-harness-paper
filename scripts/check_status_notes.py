from __future__ import annotations

from pathlib import Path


REQUIRED_NOTES = {
    Path("README.md"): ["Status And License", "dual-licensed", "MIT License", "CC BY 4.0"],
    Path("docs/artifact_release_index.md"): ["Status And License", "dual-licensed", "MIT License", "CC BY 4.0"],
    Path("docs/submission_readiness.md"): ["MIT", "CC BY 4.0", "Zenodo", "Song Luo"],
}


def main() -> None:
    findings: list[str] = []
    for path, phrases in REQUIRED_NOTES.items():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for phrase in phrases:
            if phrase not in text:
                findings.append(f"{path}: missing {phrase}")
    if findings:
        raise SystemExit("status note check failed:\n" + "\n".join(findings))
    print("status note check passed")


if __name__ == "__main__":
    main()
