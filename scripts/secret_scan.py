from __future__ import annotations

import re
from pathlib import Path


PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"gh[opusr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"Authorization:\s*Bearer\s+\S+", re.I),
]
SKIP_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache"}


def main() -> None:
    findings = []
    for path in Path(".").rglob("*"):
        if any(part in SKIP_DIRS for part in path.parts) or not path.is_file():
            continue
        if path.suffix.lower() in {".pdf", ".png", ".jpg", ".zip"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in PATTERNS:
            if pattern.search(text):
                findings.append(str(path))
                break
    if findings:
        raise SystemExit("secret-like strings found:\n" + "\n".join(findings))
    print("secret scan passed")


if __name__ == "__main__":
    main()
