from __future__ import annotations

import json
from pathlib import Path
from typing import Any


MANIFEST = Path("artifact_manifest.json")
FORBIDDEN_RUN_LOGS = [
    Path("experiments/raw/deepseek_run.out"),
    Path("experiments/raw/deepseek_run.err"),
    Path("experiments/raw/kimi_run.out"),
    Path("experiments/raw/kimi_run.err"),
]
STALE_TODO_TERMS = ["commit and push", "commit/push", "second-pass"]


def main() -> None:
    findings: list[str] = []
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for path in _manifest_paths(manifest):
        if not Path(path).exists():
            findings.append(f"manifest path missing: {path}")
    for path in FORBIDDEN_RUN_LOGS:
        if path.exists():
            findings.append(f"ignored run log should not remain in workspace: {path}")
    todo = Path("state/todo.md").read_text(encoding="utf-8").lower()
    for term in STALE_TODO_TERMS:
        if term in todo:
            findings.append(f"stale todo term found: {term}")
    if findings:
        raise SystemExit("artifact consistency check failed:\n" + "\n".join(findings))
    print("artifact consistency check passed")


def _manifest_paths(value: Any) -> list[str]:
    paths: list[str] = []
    if isinstance(value, dict):
        for item in value.values():
            paths.extend(_manifest_paths(item))
    elif isinstance(value, list):
        return []
    elif isinstance(value, str):
        if _is_external_reference(value):
            return []
        if "/" in value or "\\" in value:
            paths.append(value.rstrip("/\\"))
    return paths


def _is_external_reference(value: str) -> bool:
    return (
        value.startswith("http://")
        or value.startswith("https://")
        or value.startswith("doi:")
        or value.startswith("10.")
    )


if __name__ == "__main__":
    main()
