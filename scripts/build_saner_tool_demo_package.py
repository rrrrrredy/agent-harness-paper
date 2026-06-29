from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TRACK = "saner2027-tool-demo"
DEFAULT_OUT_DIR = ROOT / "dist" / "submissions" / TRACK
DEFAULT_PDF = ROOT / "logs" / "submission-pdfs" / TRACK / "paper" / "main.pdf"

REPOSITORY_URL = "https://github.com/rrrrrredy/agent-harness-paper/tree/v0.4.0-saner2027-tool-demo-submission"
RELEASE_URL = "https://github.com/rrrrrredy/agent-harness-paper/releases/tag/v0.1.0-preprint"
VIDEO_URL = (
    "https://github.com/rrrrrredy/agent-harness-paper/releases/download/"
    "v0.1.0-preprint/agent-harness-saner-tool-demo-video.mp4"
)
ZENODO_RECORD = "https://zenodo.org/records/20907471"
ZENODO_DOI = "10.5281/zenodo.20907471"

LOCAL_MEDIA = [
    ROOT / "dist" / "release-assets" / "agent-harness-saner-tool-demo-video.mp4",
    ROOT / "dist" / "videos" / "saner-tool-demo" / "agent-harness-demo.mp4",
    ROOT / "dist" / "release-assets" / "agent-harness-saner-tool-demo-thumbnail.png",
    ROOT / "dist" / "videos" / "saner-tool-demo" / "thumbnail.png",
]

TRACKED_EVIDENCE = [
    "artifact_manifest.json",
    "benchmark/cases.jsonl",
    "harness/__init__.py",
    "harness/core.py",
    "harness/prompts.py",
    "harness/providers.py",
    "submissions/saner2027-tool-demo/paper/main.tex",
    "submissions/saner2027-tool-demo/README.md",
    "submissions/saner2027-tool-demo/submission_package.md",
    "scripts/analyze_results.py",
    "scripts/audit_source_evidence.py",
    "scripts/build_anonymous_submission_artifact.py",
    "scripts/build_artifact_archive.py",
    "scripts/check_anonymous_submission_package.py",
    "scripts/check_archive_manifest_alignment.py",
    "scripts/check_artifact_consistency.py",
    "scripts/check_claim_traceability.py",
    "scripts/check_entrypoint_commands.py",
    "scripts/check_external_decisions.py",
    "scripts/check_public_traces.py",
    "scripts/check_release_references.py",
    "scripts/check_run_manifest_alignment.py",
    "scripts/check_status_notes.py",
    "scripts/check_tex_sources.py",
    "scripts/check_validate_workflow_paths.py",
    "scripts/generate_figures.py",
    "scripts/inspect_failures.py",
    "scripts/run_checks.py",
    "scripts/run_demo_walkthrough.py",
    "scripts/run_local_reference.py",
    "scripts/run_repo_fixture_demo.py",
    "scripts/secret_scan.py",
    "scripts/smoke_test.py",
    "tests/test_artifacts.py",
    "tests/test_harness.py",
    "experiments/raw/deepseek_live.jsonl",
    "experiments/raw/kimi_live.jsonl",
    "experiments/raw/local_reference.jsonl",
    "fixtures/repo_state_contract/contract.json",
    "fixtures/repo_state_contract/before/src/app.py",
    "fixtures/repo_state_contract/before/tests/test_app.py",
    "results/fixtures/saner_repo_fixture_summary.md",
    "results/fixtures/saner_repo_fixture_trace.json",
    "results/fixtures/saner_repo_fixture.diff",
    "results/fixtures/saner_repo_fixture_suite.md",
    "results/fixtures/saner_repo_fixture_suite.csv",
    "results/fixtures/saner_repo_fixture_suite.json",
    "results/tables/category_summary.md",
    "results/tables/experiment_summary.md",
    "results/tables/failure_taxonomy.md",
    "results/tables/live_pairwise_delta.md",
    "results/tables/live_success_uncertainty.md",
    "docs/claim_traceability.md",
    "docs/external_decision_register.md",
    "docs/reproducibility.md",
    "docs/submission_readiness.md",
    "evidence/source_audit.md",
    "evidence/source_audit.json",
]

REVIEWER_COMMANDS = [
    "python scripts/run_checks.py --mode validate",
    "python scripts/run_demo_walkthrough.py",
    "python scripts/run_repo_fixture_demo.py",
]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", default=str(DEFAULT_PDF), help="Final SANER Tool Demo PDF to copy into the package.")
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR), help="Output directory for the local submission package.")
    parser.add_argument("--validate", action="store_true", help="Only validate that the package can be generated.")
    args = parser.parse_args()

    pdf_path = Path(args.pdf)
    if not pdf_path.is_absolute():
        pdf_path = ROOT / pdf_path
    out_dir = Path(args.out_dir)
    if not out_dir.is_absolute():
        out_dir = ROOT / out_dir

    manifest = build_manifest(pdf_path, out_dir)
    if args.validate:
        print("SANER Tool Demo package validation passed")
        return

    prepare_dir(out_dir)
    pdf_out = out_dir / "paper.pdf"
    shutil.copy2(pdf_path, pdf_out)
    manifest["local_package"]["files"].insert(0, file_entry(pdf_out, out_dir))

    manifest_path = out_dir / "submission_manifest.json"
    manifest_md_path = out_dir / "submission_manifest.md"
    sums_path = out_dir / "sha256sums.txt"

    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest_md_path.write_text(render_markdown(manifest), encoding="utf-8")
    sums_path.write_text(render_sha256sums(manifest), encoding="utf-8")
    print(f"wrote {out_dir}")


def build_manifest(pdf_path: Path, out_dir: Path) -> dict[str, Any]:
    require_file(pdf_path)
    missing = [rel for rel in TRACKED_EVIDENCE if not (ROOT / rel).exists()]
    if missing:
        raise SystemExit("missing tracked evidence:\n" + "\n".join(missing))

    return {
        "track": "SANER 2027 Tool Demo",
        "title": "Replayable State-Diff Harnesses for Repository-Changing Agents",
        "author": "Song Luo",
        "submission_posture": "single-anonymous tool-demonstration submission",
        "source_revision": {
            "branch": git_value("branch", "--show-current"),
            "commit": git_value("rev-parse", "HEAD"),
            "origin": git_value("remote", "get-url", "origin"),
        },
        "public_locations": {
            "repository": REPOSITORY_URL,
            "release": RELEASE_URL,
            "screencast": VIDEO_URL,
            "zenodo_record": ZENODO_RECORD,
            "zenodo_doi": ZENODO_DOI,
        },
        "local_inputs": {
            "paper_pdf": file_entry(pdf_path, ROOT),
            "tracked_evidence": [file_entry(ROOT / rel, ROOT) for rel in TRACKED_EVIDENCE],
            "local_media_mirrors": [file_entry(path, ROOT) for path in LOCAL_MEDIA if path.exists()],
        },
        "local_package": {
            "path": relative_or_absolute(out_dir),
            "files": [],
        },
        "reviewer_commands": REVIEWER_COMMANDS,
        "inspection_points": [
            "results/fixtures/saner_repo_fixture.diff",
            "results/fixtures/saner_repo_fixture_suite.md",
            "results/tables/failure_taxonomy.md",
            "results/tables/experiment_summary.md",
        ],
    }


def prepare_dir(path: Path) -> None:
    resolved = path.resolve()
    root = (ROOT / "dist" / "submissions").resolve()
    if resolved != root and root not in resolved.parents:
        raise RuntimeError(f"refusing to clean outside submission output root: {resolved}")
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def require_file(path: Path) -> None:
    if not path.exists() or not path.is_file():
        raise SystemExit(f"required file missing: {path}")


def file_entry(path: Path, base: Path) -> dict[str, Any]:
    require_file(path)
    return {
        "path": relative_or_absolute(path, base),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def relative_or_absolute(path: Path, base: Path = ROOT) -> str:
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def git_value(*args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return result.stdout.strip()


def render_markdown(manifest: dict[str, Any]) -> str:
    source_revision = manifest["source_revision"]
    public_locations = manifest["public_locations"]
    lines = [
        "# SANER 2027 Tool Demo Submission Manifest",
        "",
        f"- Title: {manifest['title']}",
        f"- Author: {manifest['author']}",
        f"- Track: {manifest['track']}",
        f"- Source branch: `{source_revision['branch']}`",
        f"- Source commit: `{source_revision['commit']}`",
        f"- Repository: {public_locations['repository']}",
        f"- Zenodo: {public_locations['zenodo_record']} ({public_locations['zenodo_doi']})",
        f"- Screencast: {public_locations['screencast']}",
        f"- Release: {public_locations['release']}",
        "",
        "## Local Package Files",
        "",
        "| File | Bytes | SHA-256 |",
        "|---|---:|---|",
    ]
    for entry in manifest["local_package"]["files"]:
        lines.append(f"| `{entry['path']}` | {entry['bytes']} | `{entry['sha256']}` |")

    lines.extend(
        [
            "",
            "## Local Inputs",
            "",
            "| Input | Bytes | SHA-256 |",
            "|---|---:|---|",
        ]
    )
    lines.append(_entry_row(manifest["local_inputs"]["paper_pdf"]))
    for entry in manifest["local_inputs"]["local_media_mirrors"]:
        lines.append(_entry_row(entry))

    lines.extend(
        [
            "",
            "## Tracked Evidence",
            "",
            "| Input | Bytes | SHA-256 |",
            "|---|---:|---|",
        ]
    )
    for entry in manifest["local_inputs"]["tracked_evidence"]:
        lines.append(_entry_row(entry))

    lines.extend(["", "## Reviewer Commands", ""])
    for command in manifest["reviewer_commands"]:
        lines.append(f"- `{command}`")
    lines.append("")
    return "\n".join(lines)


def _entry_row(entry: dict[str, Any]) -> str:
    return f"| `{entry['path']}` | {entry['bytes']} | `{entry['sha256']}` |"


def render_sha256sums(manifest: dict[str, Any]) -> str:
    entries = [*manifest["local_package"]["files"], manifest["local_inputs"]["paper_pdf"]]
    entries.extend(manifest["local_inputs"]["local_media_mirrors"])
    entries.extend(manifest["local_inputs"]["tracked_evidence"])
    seen: set[str] = set()
    lines: list[str] = []
    for entry in entries:
        key = entry["path"]
        if key in seen:
            continue
        seen.add(key)
        lines.append(f"{entry['sha256']}  {entry['path']}")
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    main()
