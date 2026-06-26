from __future__ import annotations

import argparse
import subprocess
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = Path("dist/agent-harness-paper-artifact.zip")

EXCLUDED_PREFIXES = (
    "state/",
    "logs/",
    ".venv/",
    "dist/",
    "__pycache__/",
    ".pytest_cache/",
)

EXCLUDED_SUFFIXES = (
    ".pyc",
    ".log",
    ".aux",
    ".bbl",
    ".blg",
    ".fls",
    ".fdb_latexmk",
    ".out",
    ".synctex.gz",
    ".toc",
    ".pdf",
)

EXCLUDED_NAMES = {
    ".env",
    "local-secrets.env",
}

REQUIRED_ARCHIVE_FILES = [
    "README.md",
    "artifact_manifest.json",
    "paper/main.tex",
    "paper/references.bib",
    "paper/metadata.json",
    "benchmark/cases.jsonl",
    "harness/core.py",
    "harness/providers.py",
    "experiments/run_manifest.md",
    "docs/artifact_release_index.md",
    "docs/claim_traceability.md",
    "docs/data_dictionary.md",
    "docs/external_decision_register.md",
    "docs/live_rerun_promotion.md",
    "docs/reproducibility.md",
    "docs/submission_readiness.md",
    "evidence/github_snapshots.md",
    "evidence/source_audit.md",
    "results/tables/experiment_summary.md",
    "figures/success_by_variant.svg",
    ".github/workflows/latex.yml",
    ".github/workflows/validate.yml",
    "scripts/check_provider_credentials.py",
    "scripts/check_claim_traceability.py",
    "scripts/check_external_decisions.py",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Validate archive file selection without writing a zip.")
    parser.add_argument("--list", action="store_true", help="Print archive file paths.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Zip output path.")
    args = parser.parse_args()

    files = archive_files()
    validate_selection(files)

    if args.list:
        for path in files:
            print(path)
    if args.check:
        print(f"archive selection check passed: {len(files)} files")
        return

    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for rel_path in files:
            archive.write(ROOT / rel_path, rel_path)
    print(f"wrote {output} with {len(files)} files")


def archive_files() -> list[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    return sorted(path for path in result.stdout.splitlines() if include_path(path))


def include_path(path: str) -> bool:
    normalized = path.replace("\\", "/")
    if normalized in EXCLUDED_NAMES:
        return False
    if normalized.startswith(".env."):
        return False
    if any(normalized.startswith(prefix) for prefix in EXCLUDED_PREFIXES):
        return False
    if normalized.startswith("paper/") and normalized.endswith(".pdf"):
        return False
    if normalized.startswith("experiments/raw/") and normalized.endswith((".out", ".err")):
        return False
    if normalized.endswith(EXCLUDED_SUFFIXES):
        return False
    return True


def validate_selection(files: list[str]) -> None:
    file_set = set(files)
    findings = []
    for required in REQUIRED_ARCHIVE_FILES:
        if required not in file_set:
            findings.append(f"missing required archive file: {required}")
    for path in files:
        if not include_path(path):
            findings.append(f"excluded path selected: {path}")
    if any(path.startswith("state/") for path in files):
        findings.append("state files must not be included in archive bundle")
    if findings:
        raise SystemExit("archive selection check failed:\n" + "\n".join(findings))


if __name__ == "__main__":
    main()
