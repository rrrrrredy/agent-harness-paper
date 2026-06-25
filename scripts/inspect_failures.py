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
                            "invalid_tool_calls": row["invalid_tool_calls"],
                            "permission_violations": row["permission_violations"],
                            "routing_errors": row["over_under_trigger_error"],
                            "notes": "; ".join(row.get("notes", [])[:3]),
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


if __name__ == "__main__":
    main()
