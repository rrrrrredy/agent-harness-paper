from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import zipfile


ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = ROOT / "dist" / "anonymous"

COMMON_INCLUDE_FILES = [
    "pyproject.toml",
    "benchmark/cases.jsonl",
    "harness/__init__.py",
    "harness/core.py",
    "harness/prompts.py",
    "harness/providers.py",
    "scripts/analyze_results.py",
    "scripts/run_demo_walkthrough.py",
    "scripts/run_local_reference.py",
    "scripts/run_repo_fixture_demo.py",
    "scripts/smoke_test.py",
    "tests/test_harness.py",
    "tests/test_artifacts.py",
    "experiments/raw/local_reference.jsonl",
    "experiments/raw/deepseek_live.jsonl",
    "experiments/raw/kimi_live.jsonl",
    "results/tables/experiment_summary.csv",
    "results/tables/experiment_summary.md",
    "results/tables/category_summary.csv",
    "results/tables/category_summary.md",
    "results/tables/failure_taxonomy.csv",
    "results/tables/failure_taxonomy.md",
    "results/tables/live_success_uncertainty.csv",
    "results/tables/live_success_uncertainty.md",
    "results/tables/live_pairwise_delta.csv",
    "results/tables/live_pairwise_delta.md",
    "results/fixtures/saner_repo_fixture_summary.md",
    "results/fixtures/saner_repo_fixture_trace.json",
    "results/fixtures/saner_repo_fixture.diff",
    "results/fixtures/saner_repo_fixture_suite.md",
    "results/fixtures/saner_repo_fixture_suite.csv",
    "results/fixtures/saner_repo_fixture_suite.json",
    "fixtures/repo_state_contract/contract.json",
    "fixtures/repo_state_contract/before/src/app.py",
    "fixtures/repo_state_contract/before/tests/test_app.py",
]

TRACK_FILES = {
    "icse2027-nier": ["submissions/icse2027-nier/paper/main.tex"],
    "saner2027-short-paper": ["submissions/saner2027-short-paper/paper/main.tex"],
}

DEANON_PATTERNS = [
    "Song Luo",
    "Luo, Song",
    "luosong",
    "rrrrrredy",
    "github.com/rrrrrredy",
    "zenodo.org/records/20907471",
    "10.5281/zenodo",
    "arxiv.org/auth/endorse",
]

README_TEMPLATE = """# Anonymous Supplemental Artifact

This anonymous package accompanies the {track_label} submission on stateful
AI-agent harnesses.

The package contains:

- 24 case definitions for trigger/routing, stateful tool use, permission and
  injection behavior, memory scoping, and replay/failure recovery;
- a small Python harness with mock tools, state assertions, and metric
  computation;
- deterministic local-reference rows and recorded live-provider rows;
- regenerated tables used for the pilot discussion;
- a small repository fixture suite with success and failure scenarios;
- the anonymous LaTeX source for the selected track.

No live provider credentials are required for the reviewer path.

## Quick Check

```powershell
python scripts/run_demo_walkthrough.py
python scripts/smoke_test.py
```

The walkthrough loads all cases, evaluates one security case through the
reference policy, regenerates deterministic reference rows, and rebuilds the
aggregate tables.

For the repository-fixture suite, run:

```powershell
python scripts/run_repo_fixture_demo.py
```

If `pytest` is available, `python -m pytest -q` can also be run, but it is not
required for the no-dependency reviewer path.

## Scope

This package is not a model leaderboard. The case set is small and synthetic;
the recorded provider rows are pilot evidence for the evaluation shape only.
The intended review question is whether state-diff contracts make agent
failures inspectable beyond final-answer correctness.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--track",
        default="icse2027-nier",
        choices=sorted(TRACK_FILES),
        help="Anonymous submission package to build.",
    )
    args = parser.parse_args()

    out_dir = OUT_ROOT / args.track
    zip_path = OUT_ROOT / f"{args.track}-anonymous-artifact.zip"
    prepare_dir(out_dir)

    for rel in [*COMMON_INCLUDE_FILES, *TRACK_FILES[args.track]]:
        copy_file(rel, out_dir)

    (out_dir / "README.md").write_text(readme_for(args.track), encoding="utf-8")
    write_manifest(out_dir)
    assert_anonymous(out_dir)
    build_zip(out_dir, zip_path)
    print(f"wrote {zip_path}")


def readme_for(track: str) -> str:
    labels = {
        "icse2027-nier": "ICSE 2027 NIER",
        "saner2027-short-paper": "SANER 2027 Short Paper",
    }
    return README_TEMPLATE.format(track_label=labels[track])


def prepare_dir(path: Path) -> None:
    resolved = path.resolve()
    out_root = OUT_ROOT.resolve()
    if out_root not in resolved.parents and resolved != out_root:
        raise RuntimeError(f"refusing to clean outside output root: {resolved}")
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def copy_file(rel: str, out_dir: Path) -> None:
    src = ROOT / rel
    if not src.exists():
        raise FileNotFoundError(rel)
    dst = out_dir / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def write_manifest(out_dir: Path) -> None:
    entries = []
    for path in sorted(p for p in out_dir.rglob("*") if p.is_file()):
        rel = path.relative_to(out_dir).as_posix()
        entries.append(f"- `{rel}`")
    (out_dir / "MANIFEST.md").write_text(
        "# Anonymous Artifact Manifest\n\n" + "\n".join(entries) + "\n",
        encoding="utf-8",
    )


def assert_anonymous(out_dir: Path) -> None:
    findings: list[str] = []
    for path in sorted(p for p in out_dir.rglob("*") if p.is_file()):
        if path.suffix.lower() in {".pyc", ".png", ".mp4", ".zip"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in DEANON_PATTERNS:
            if pattern.lower() in text.lower():
                findings.append(f"{path.relative_to(out_dir)} contains {pattern}")
    if findings:
        raise RuntimeError("anonymous artifact check failed:\n" + "\n".join(findings))


def build_zip(out_dir: Path, zip_path: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(p for p in out_dir.rglob("*") if p.is_file()):
            archive.write(path, path.relative_to(out_dir).as_posix())


if __name__ == "__main__":
    main()
