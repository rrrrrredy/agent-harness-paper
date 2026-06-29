from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

from build_anonymous_submission_artifact import (
    DEANON_PATTERNS,
    OUT_ROOT,
    ROOT,
    TRACK_FILES,
    include_files,
)


FORBIDDEN_PREFIXES = (
    ".git/",
    "dist/",
    "logs/",
    "state/",
)

FORBIDDEN_FILENAMES = {
    ".env",
    "local-secrets.env",
}

TEXT_SUFFIXES = {
    ".bib",
    ".cff",
    ".csv",
    ".json",
    ".jsonl",
    ".md",
    ".py",
    ".tex",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--track",
        required=True,
        choices=sorted(TRACK_FILES),
        help="Anonymous package track to verify.",
    )
    parser.add_argument("--zip", dest="zip_path", help="Package path. Defaults to dist/anonymous/<track>-anonymous-artifact.zip.")
    parser.add_argument("--build", action="store_true", help="Rebuild the anonymous package before checking it.")
    parser.add_argument("--run-smoke", action="store_true", help="Extract the package and run reviewer smoke commands.")
    args = parser.parse_args()

    zip_path = Path(args.zip_path) if args.zip_path else OUT_ROOT / f"{args.track}-anonymous-artifact.zip"
    if not zip_path.is_absolute():
        zip_path = ROOT / zip_path

    if args.build:
        subprocess.run(
            [sys.executable, "scripts/build_anonymous_submission_artifact.py", "--track", args.track],
            cwd=ROOT,
            check=True,
        )

    findings = check_zip(args.track, zip_path)
    if args.run_smoke and not findings:
        findings.extend(run_smoke(args.track, zip_path))

    if findings:
        raise SystemExit("anonymous package check failed:\n" + "\n".join(f"- {item}" for item in findings))
    print(f"anonymous package check passed: {zip_path}")


def check_zip(track: str, zip_path: Path) -> list[str]:
    findings: list[str] = []
    if not zip_path.exists():
        return [f"zip missing: {zip_path}"]

    required = {*include_files(track), "README.md", "MANIFEST.md"}
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
        name_set = set(names)
        for name in sorted(required):
            if name not in name_set:
                findings.append(f"missing required file: {name}")
        for name in names:
            normalized = name.replace("\\", "/")
            findings.extend(check_path(normalized))
            findings.extend(check_deanon_in_name(normalized))
            if Path(normalized).suffix.lower() in TEXT_SUFFIXES:
                with archive.open(name) as handle:
                    text = handle.read().decode("utf-8", errors="ignore")
                findings.extend(check_deanon_in_text(normalized, text))
    return findings


def check_path(name: str) -> list[str]:
    findings: list[str] = []
    path = Path(name)
    if path.is_absolute() or ".." in path.parts:
        findings.append(f"unsafe archive path: {name}")
    if name.endswith("/"):
        return findings
    if any(name.startswith(prefix) for prefix in FORBIDDEN_PREFIXES):
        findings.append(f"forbidden archive prefix: {name}")
    if Path(name).name in FORBIDDEN_FILENAMES:
        findings.append(f"forbidden file name: {name}")
    if name.lower().endswith((".pdf", ".aux", ".bbl", ".blg", ".log", ".out")):
        findings.append(f"compiled or transient file should not be in anonymous package: {name}")
    return findings


def check_deanon_in_name(name: str) -> list[str]:
    lowered = name.lower()
    return [f"path contains identifying pattern `{pattern}`: {name}" for pattern in DEANON_PATTERNS if pattern.lower() in lowered]


def check_deanon_in_text(name: str, text: str) -> list[str]:
    lowered = text.lower()
    return [f"{name} contains identifying pattern `{pattern}`" for pattern in DEANON_PATTERNS if pattern.lower() in lowered]


def run_smoke(track: str, zip_path: Path) -> list[str]:
    findings: list[str] = []
    with tempfile.TemporaryDirectory(prefix=f"{track}-artifact-") as temp_root:
        extract_dir = Path(temp_root) / "artifact"
        extract_dir.mkdir()
        with zipfile.ZipFile(zip_path) as archive:
            for name in archive.namelist():
                if check_path(name):
                    findings.append(f"refusing to extract unsafe path: {name}")
                    continue
                archive.extract(name, extract_dir)
        if findings:
            return findings
        for command in reviewer_commands(track):
            result = subprocess.run(command, cwd=extract_dir, text=True, capture_output=True, timeout=120)
            if result.returncode != 0:
                findings.append(
                    "smoke command failed: "
                    + " ".join(command)
                    + f"\nstdout:\n{result.stdout}\nstderr:\n{result.stderr}"
                )
    return findings


def reviewer_commands(track: str) -> list[list[str]]:
    commands = [
        [sys.executable, "scripts/run_demo_walkthrough.py"],
        [sys.executable, "scripts/smoke_test.py"],
    ]
    if track == "saner2027-short-paper":
        commands.append([sys.executable, "scripts/run_repo_fixture_demo.py"])
    return commands


if __name__ == "__main__":
    main()
