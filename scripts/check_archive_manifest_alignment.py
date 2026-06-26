from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from build_artifact_archive import archive_files


MANIFEST = Path("artifact_manifest.json")


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    selected = set(archive_files())
    findings: list[str] = []

    for manifest_path in sorted(_manifest_paths(manifest)):
        normalized = manifest_path.replace("\\", "/").rstrip("/")
        path = Path(normalized)
        if path.is_file():
            if normalized not in selected:
                findings.append(f"manifest file missing from archive selection: {normalized}")
        elif path.is_dir():
            prefix = normalized + "/"
            if not any(selected_path.startswith(prefix) for selected_path in selected):
                findings.append(f"manifest directory absent from archive selection: {normalized}")
        else:
            findings.append(f"manifest path does not exist: {normalized}")

    if findings:
        raise SystemExit("archive manifest alignment check failed:\n" + "\n".join(findings))
    print(f"archive manifest alignment check passed: {len(selected)} selected files")


def _manifest_paths(value: Any) -> set[str]:
    paths: set[str] = set()
    if isinstance(value, dict):
        for item in value.values():
            paths.update(_manifest_paths(item))
    elif isinstance(value, list):
        return paths
    elif isinstance(value, str):
        if "/" in value or "\\" in value:
            paths.add(value)
    return paths


if __name__ == "__main__":
    main()
