from __future__ import annotations

import json
import re
from pathlib import Path


PUBLIC_RELEASE_FILES = [
    Path("artifact_manifest.json"),
    Path("docs/artifact_release_index.md"),
    Path("docs/final_cleanup.md"),
    Path("docs/reproducibility.md"),
]


def main() -> None:
    manifest = json.loads(Path("artifact_manifest.json").read_text(encoding="utf-8"))
    release_status = manifest["release_status"]
    pdf_run = release_status["latest_checked_pdf_run"]
    pdf_artifact = release_status["pdf_artifact_name"]
    validation_workflow = release_status["validation_workflow"]

    findings: list[str] = []
    if "latest_checked_validation_run" in release_status:
        findings.append("artifact_manifest.json: validation run IDs should not be committed")
    for path in PUBLIC_RELEASE_FILES:
        text = path.read_text(encoding="utf-8", errors="ignore")
        if "Latest checked validation run" in text:
            findings.append(f"{path}: remove moving validation run ID")
        if "latest_checked_validation_run" in text:
            findings.append(f"{path}: remove moving validation run key")
        for run_id in re.findall(r"gh run download (\d+)", text):
            if run_id != pdf_run:
                findings.append(f"{path}: PDF download run {run_id} does not match manifest {pdf_run}")
        for run_id in re.findall(r"Latest checked PDF run: `(\d+)`", text):
            if run_id != pdf_run:
                findings.append(f"{path}: checked PDF run {run_id} does not match manifest {pdf_run}")

    release_index = Path("docs/artifact_release_index.md").read_text(encoding="utf-8")
    if pdf_run not in release_index:
        findings.append("docs/artifact_release_index.md: missing PDF run ID")
    if pdf_artifact not in release_index:
        findings.append("docs/artifact_release_index.md: missing PDF artifact name")
    if validation_workflow not in release_index:
        findings.append("docs/artifact_release_index.md: missing validation workflow path")

    if findings:
        raise SystemExit("release reference check failed:\n" + "\n".join(findings))
    print("release reference check passed")


if __name__ == "__main__":
    main()
