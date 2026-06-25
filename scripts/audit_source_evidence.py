from __future__ import annotations

import json
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


IN_JSON = Path("evidence/github_evidence.json")
OUT_JSON = Path("evidence/source_audit.json")
OUT_MD = Path("evidence/source_audit.md")
MAX_FETCHED_FILES_PER_REPO = 12

CANDIDATE_PARTS = {
    "readme",
    "skill.md",
    "agents.md",
    "docs",
    "test",
    "tests",
    "scripts",
    "benchmark",
    "benchmarks",
    "eval",
    "evals",
    "security",
    "memory",
    "audit",
    "cron",
}

SIGNALS = {
    "routing_contract": ("routing", "trigger", "use when", "description:", "input", "output"),
    "state_diff": ("state", "diff", "snapshot", "changed", "final state"),
    "permission_policy": ("permission", "allowed", "forbidden", "dry-run", "dry run", "approval"),
    "review_gate": ("review", "approve", "approval", "candidate", "publish"),
    "memory_scope": ("memory", "forget", "scop", "local", "repo"),
    "security": ("secret", "prompt injection", "injection", ".env", "token", "unsafe"),
    "replay": ("replay", "trace", "rerun", "recover"),
    "testing": ("pytest", "test", "benchmark", "eval", "ci"),
    "observability": ("log", "audit", "metric", "telemetry", "report"),
}


def main() -> None:
    snapshot = json.loads(IN_JSON.read_text(encoding="utf-8"))
    audits = []
    for repo in snapshot.get("first_party_repositories", []):
        name = repo["nameWithOwner"]
        branch = (repo.get("defaultBranchRef") or {}).get("name") or "main"
        try:
            tree = _tree(name, branch)
            files = [item["path"] for item in tree.get("tree", []) if item.get("type") == "blob"]
            candidate_paths = sorted((path for path in files if _is_candidate(path)), key=_priority)
            candidates = [_audit_file(name, branch, path) for path in candidate_paths[:MAX_FETCHED_FILES_PER_REPO]]
            for path in candidate_paths[MAX_FETCHED_FILES_PER_REPO:]:
                path_only = _audit_path_only(path)
                if path_only["signals"]:
                    candidates.append(path_only)
            candidates = [item for item in candidates if item["signals"]]
            audits.append(
                {
                    "repository": name,
                    "private": bool(repo.get("isPrivate")),
                    "fork": bool(repo.get("isFork")),
                    "default_branch": branch,
                    "candidate_file_count": len(candidates),
                    "signal_counts": _count_signals(candidates),
                    "files": candidates[:40],
                }
            )
            print(f"audited {name}: {len(candidates)} signal files")
        except Exception as exc:
            audits.append(
                {
                    "repository": name,
                    "private": bool(repo.get("isPrivate")),
                    "fork": bool(repo.get("isFork")),
                    "default_branch": branch,
                    "error": str(exc),
                    "candidate_file_count": 0,
                    "signal_counts": {},
                    "files": [],
                }
            )
            print(f"failed {name}: {exc}")
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "method": "Path and keyword-signal audit using GitHub API. Source file bodies are not stored.",
        "repositories": audits,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(_markdown(payload), encoding="utf-8")
    print(f"wrote {OUT_JSON} and {OUT_MD}")


def _gh(args: list[str]) -> Any:
    proc = subprocess.run(
        ["gh", "api", *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=25,
    )
    return json.loads(proc.stdout)


def _tree(repo: str, branch: str) -> dict[str, Any]:
    return _gh([f"repos/{repo}/git/trees/{branch}?recursive=1"])


def _is_candidate(path: str) -> bool:
    lower = path.lower()
    if lower.endswith((".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".lock")):
        return False
    parts = set(lower.replace("\\", "/").split("/"))
    return any(part in lower for part in CANDIDATE_PARTS) or bool(parts & CANDIDATE_PARTS)


def _audit_file(repo: str, branch: str, path: str) -> dict[str, Any]:
    content = ""
    if _should_fetch(path):
        try:
            response = subprocess.run(
                ["gh", "api", f"repos/{repo}/contents/{path}", "-f", f"ref={branch}", "--jq", ".content"],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=20,
            )
            import base64

            content = base64.b64decode(response.stdout.strip()).decode("utf-8", errors="ignore")
        except Exception:
            content = ""
    haystack = (path + "\n" + content[:20000]).lower()
    signals = sorted(name for name, words in SIGNALS.items() if any(word in haystack for word in words))
    return {"path": path, "signals": signals}


def _audit_path_only(path: str) -> dict[str, Any]:
    haystack = path.lower()
    signals = sorted(name for name, words in SIGNALS.items() if any(word in haystack for word in words))
    return {"path": path, "signals": signals, "path_only": True}


def _should_fetch(path: str) -> bool:
    lower = path.lower()
    return lower.endswith((".md", ".txt", ".yml", ".yaml", ".toml", ".json", ".py", ".ts", ".tsx", ".js", ".mjs"))


def _priority(path: str) -> tuple[int, str]:
    lower = path.lower()
    if lower.endswith("skill.md"):
        return (0, lower)
    if lower.endswith("readme.md"):
        return (1, lower)
    if "test" in lower or "eval" in lower or "benchmark" in lower:
        return (2, lower)
    if "docs/" in lower or lower.startswith("docs/"):
        return (3, lower)
    return (4, lower)


def _count_signals(files: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for file in files:
        for signal in file["signals"]:
            counts[signal] += 1
    return dict(sorted(counts.items()))


def _markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Source Evidence Audit",
        "",
        f"Generated at: `{payload['generated_at']}`",
        "",
        payload["method"],
        "",
        "This audit supports bounded artifact claims. It records repository paths and signal categories, not source excerpts.",
        "",
        "| Repository | Private | Fork | Signal files | Top signals | Representative paths |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for repo in payload["repositories"]:
        counts = repo.get("signal_counts") or {}
        top = ", ".join(f"{key}={value}" for key, value in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:5])
        paths = ", ".join(file["path"] for file in repo.get("files", [])[:5])
        if repo.get("error"):
            paths = "ERROR: " + repo["error"]
        lines.append(
            "| "
            + " | ".join(
                [
                    repo["repository"],
                    str(repo.get("private", "")),
                    str(repo.get("fork", "")),
                    str(repo.get("candidate_file_count", 0)),
                    _cell(top),
                    _cell(paths),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def _cell(value: str) -> str:
    return value.replace("|", "/").replace("\n", " ").strip()


if __name__ == "__main__":
    main()
