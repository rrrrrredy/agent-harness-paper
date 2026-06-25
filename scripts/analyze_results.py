from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path


RAW = Path("experiments/raw")
OUT = Path("results/tables")


def load_rows() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(RAW.glob("*.jsonl")):
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    rows.append(json.loads(line))
    return rows


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = load_rows()
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[(row["provider"], row["variant"])].append(row)

    summary = []
    for (provider, variant), items in sorted(grouped.items()):
        n = len(items)
        provider_errors = [i for i in items if any(_is_provider_error(str(note)) for note in i.get("notes", []))]
        parse_errors = [i for i in items if any(_is_parse_error(str(note)) for note in i.get("notes", []))]
        executed = [i for i in items if i not in provider_errors]
        denom = len(executed) or 1
        summary.append(
            {
                "provider": provider,
                "variant": variant,
                "n_total": n,
                "n_executed": len(executed),
                "provider_errors": len(provider_errors),
                "parse_errors": len(parse_errors),
                "task_success_rate": round(sum(i["task_success"] for i in executed) / denom, 3),
                "state_diff_rate": round(sum(i["state_diff_correct"] for i in executed) / denom, 3),
                "permission_violations": sum(i["permission_violations"] for i in executed),
                "invalid_tool_calls": sum(i["invalid_tool_calls"] for i in executed),
                "unsafe_secret_access": sum(i["unsafe_secret_access"] for i in executed),
                "routing_errors": sum(i["over_under_trigger_error"] for i in executed),
                "recovery_rate": round(sum(i["recovered"] for i in executed) / denom, 3),
            }
        )

    write_csv(OUT / "experiment_summary.csv", summary)
    write_md(OUT / "experiment_summary.md", summary)
    write_tex(OUT / "experiment_summary.tex", summary)
    print(f"analyzed {len(rows)} rows")


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_md(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("No experiment rows found.\n", encoding="utf-8")
        return
    headers = list(rows[0])
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[h]) for h in headers) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_tex(path: Path, rows: list[dict]) -> None:
    if not rows:
        path.write_text("% No experiment rows found.\n", encoding="utf-8")
        return
    lines = [
        "\\begin{tabular}{llrrrrrr}",
        "\\toprule",
        "Provider & Variant & Total & Executed & Provider errors & Parse errors & Success & Violations \\\\",
        "\\midrule",
    ]
    for row in rows:
        lines.append(
            f"{_tex(str(row['provider']))} & {_tex(str(row['variant']).replace('_', ' '))} & "
            f"{row['n_total']} & {row['n_executed']} & {row['provider_errors']} & "
            f"{row['parse_errors']} & {row['task_success_rate']:.3f} & {row['permission_violations']} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _is_provider_error(note: str) -> bool:
    if not note.startswith("provider_error:"):
        return False
    markers = ("HTTP", "missing environment", "Invalid Authentication", "authentication", "rate limit")
    return any(marker.lower() in note.lower() for marker in markers)


def _is_parse_error(note: str) -> bool:
    return note.startswith("provider_error:") and not _is_provider_error(note)


def _tex(value: str) -> str:
    return (
        value.replace("\\", "\\textbackslash{}")
        .replace("_", "\\_")
        .replace("&", "\\&")
        .replace("%", "\\%")
        .replace("#", "\\#")
    )


if __name__ == "__main__":
    main()
