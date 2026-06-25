from __future__ import annotations

import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


FIRST_PARTY_REPOS = [
    "rrrrrredy/skillops-paper",
    "rrrrrredy/skill-design-guide",
    "rrrrrredy/skill-security-guard",
    "rrrrrredy/persistent-memory",
    "rrrrrredy/agent-self-audit",
    "rrrrrredy/ai-radar-web",
    "rrrrrredy/ai-radar-skill",
    "rrrrrredy/lobster-guard",
    "rrrrrredy/all-net-search-read",
    "rrrrrredy/ai-talent-graph",
    "rrrrrredy/ai-info-radar",
    "rrrrrredy/book-hunter",
    "rrrrrredy/x-twitter-scraper",
    "rrrrrredy/xiaoyuzhou-podcast",
    "rrrrrredy/weibo-scraper",
    "rrrrrredy/wechat-reader",
    "rrrrrredy/bilibili-video",
    "rrrrrredy/ai-talent-radar",
    "rrrrrredy/agent-job-monitor",
]

UPSTREAM_PRS = [
    ("openclaw/openclaw", 93149),
    ("openclaw/openclaw", 69975),
    ("openclaw/openclaw", 70046),
    ("openclaw/openclaw", 59488),
    ("openclaw/openclaw", 59637),
    ("openclaw/openclaw", 69199),
    ("NousResearch/hermes-agent", 47094),
    ("NousResearch/hermes-agent", 47589),
]

OUT_JSON = Path("evidence/github_evidence.json")
OUT_MD = Path("evidence/github_snapshots.md")


def main() -> None:
    snapshot = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "first_party_repositories": [_repo(repo) for repo in FIRST_PARTY_REPOS],
        "upstream_pull_requests": [_pr(repo, number) for repo, number in UPSTREAM_PRS],
    }
    OUT_JSON.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUT_MD.write_text(_markdown(snapshot), encoding="utf-8")
    print(f"wrote {OUT_JSON} and {OUT_MD}")


def _gh(args: list[str]) -> Any:
    proc = subprocess.run(["gh", *args], check=True, capture_output=True, text=True, encoding="utf-8")
    return json.loads(proc.stdout)


def _repo(name: str) -> dict[str, Any]:
    data = _gh(
        [
            "repo",
            "view",
            name,
            "--json",
            "nameWithOwner,description,isFork,isPrivate,url,defaultBranchRef,createdAt,updatedAt,primaryLanguage,repositoryTopics",
        ]
    )
    topics = data.get("repositoryTopics") or []
    data["topic_names"] = [item.get("name", "") for item in topics]
    data.pop("repositoryTopics", None)
    return data


def _pr(repo: str, number: int) -> dict[str, Any]:
    data = _gh(
        [
            "pr",
            "view",
            str(number),
            "--repo",
            repo,
            "--json",
            "title,body,files,additions,deletions,commits,state,isDraft,url,createdAt,updatedAt,closedAt",
        ]
    )
    body = data.get("body") or ""
    data["repository"] = repo
    data["number"] = number
    data["body_excerpt"] = body[:1500]
    data.pop("body", None)
    data["files"] = [
        {
            "path": item.get("path"),
            "additions": item.get("additions"),
            "deletions": item.get("deletions"),
            "changeType": item.get("changeType"),
        }
        for item in data.get("files", [])
    ]
    data["commits"] = [
        {
            "oid": item.get("oid"),
            "messageHeadline": item.get("messageHeadline"),
            "authoredDate": item.get("authoredDate"),
        }
        for item in data.get("commits", [])
    ]
    return data


def _markdown(snapshot: dict[str, Any]) -> str:
    lines = [
        "# GitHub Evidence Snapshots",
        "",
        f"Generated at: `{snapshot['generated_at']}`",
        "",
        "## First-Party Repositories",
        "",
        "| Repository | Private | Fork | Language | Updated | Description |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for repo in snapshot["first_party_repositories"]:
        language = (repo.get("primaryLanguage") or {}).get("name") or ""
        lines.append(
            "| "
            + " | ".join(
                [
                    f"[{repo['nameWithOwner']}]({repo['url']})",
                    str(repo.get("isPrivate", "")),
                    str(repo.get("isFork", "")),
                    language,
                    repo.get("updatedAt", ""),
                    _cell(repo.get("description") or ""),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Upstream Pull Requests",
            "",
            "| PR | State | Additions | Deletions | Files | Evidence relevance |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for pr in snapshot["upstream_pull_requests"]:
        files = ", ".join(item["path"] for item in pr.get("files", [])[:5])
        relevance = _summarize_relevance(pr)
        lines.append(
            "| "
            + " | ".join(
                [
                    f"[{pr['repository']}#{pr['number']}]({pr['url']})",
                    pr.get("state", ""),
                    str(pr.get("additions", "")),
                    str(pr.get("deletions", "")),
                    _cell(files),
                    _cell(relevance),
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def _summarize_relevance(pr: dict[str, Any]) -> str:
    title = pr.get("title", "").lower()
    body = pr.get("body_excerpt", "").lower()
    text = title + "\n" + body
    if "dry-run" in text or "dry run" in text:
        return "Preview before side effect; mutation boundary evidence."
    if "session" in text or "recall" in text:
        return "State continuity or scoped memory recall evidence."
    if "timezone" in text or "--tz" in text or "time-only" in text:
        return "Scheduler contract and temporal semantics evidence."
    if "memory" in text or "sqlite" in text:
        return "Recoverable memory/runtime boundary evidence."
    return "Upstream agent-runtime boundary evidence."


def _cell(value: str) -> str:
    return value.replace("|", "/").replace("\n", " ").strip()


if __name__ == "__main__":
    main()
