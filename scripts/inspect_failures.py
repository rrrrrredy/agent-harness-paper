from __future__ import annotations

import json
from pathlib import Path


def main() -> None:
    rows = []
    for path in sorted(Path("experiments/raw").glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                if not row.get("task_success") or row.get("permission_violations"):
                    rows.append(
                        {
                            "provider": row["provider"],
                            "variant": row["variant"],
                            "case_id": row["case_id"],
                            "category": row["category"],
                            "error_class": _error_class(row.get("notes", [])),
                            "invalid_tool_calls": row["invalid_tool_calls"],
                            "permission_violations": row["permission_violations"],
                            "routing_errors": row["over_under_trigger_error"],
                            "notes": "; ".join(_display_notes(row.get("notes", []))[:3]),
                        }
                    )
    out = Path("results/tables/failure_inspection.md")
    out.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        out.write_text("No failures found.\n", encoding="utf-8")
    else:
        headers = list(rows[0])
        lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
        for row in rows:
            lines.append("| " + " | ".join(str(row[h]).replace("|", "/") for h in headers) + " |")
        out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(rows)} rows)")


def _error_class(notes: list[str]) -> str:
    if any(_is_provider_error(str(note)) for note in notes):
        return "provider_error"
    if any(_is_parse_error(str(note)) for note in notes):
        return "parse_error"
    return "behavior"


def _display_notes(notes: list[str]) -> list[str]:
    display = []
    for note in notes:
        text = str(note)
        if _is_parse_error(text) and text.startswith("provider_error:"):
            display.append("parse_error:" + text.split(":", 1)[1])
        else:
            display.append(text)
    return display


def _is_provider_error(note: str) -> bool:
    if not note.startswith("provider_error:"):
        return False
    markers = ("http", "missing environment", "invalid authentication", "authentication", "rate limit")
    return any(marker in note.lower() for marker in markers)


def _is_parse_error(note: str) -> bool:
    if note.startswith("parse_error:"):
        return True
    return note.startswith("provider_error:") and not _is_provider_error(note)


if __name__ == "__main__":
    main()
