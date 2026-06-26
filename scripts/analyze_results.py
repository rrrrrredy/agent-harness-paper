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
    category_rows = category_summary(rows)
    write_csv(OUT / "category_summary.csv", category_rows)
    write_md(OUT / "category_summary.md", category_rows)
    write_category_tex(OUT / "category_summary.tex", category_rows)
    taxonomy_rows = failure_taxonomy(rows)
    write_csv(OUT / "failure_taxonomy.csv", taxonomy_rows)
    write_md(OUT / "failure_taxonomy.md", taxonomy_rows)
    write_failure_taxonomy_tex(OUT / "failure_taxonomy.tex", taxonomy_rows)
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


def category_summary(rows: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[(row["provider"], row["variant"], row["category"])].append(row)
    out = []
    for (provider, variant, category), items in sorted(grouped.items()):
        executable = [row for row in items if not any(_is_provider_error(str(note)) for note in row.get("notes", []))]
        denom = len(executable) or 1
        out.append(
            {
                "provider": provider,
                "variant": variant,
                "category": category,
                "n_total": len(items),
                "n_executed": len(executable),
                "success_rate": round(sum(row["task_success"] for row in executable) / denom, 3),
                "state_diff_rate": round(sum(row["state_diff_correct"] for row in executable) / denom, 3),
                "routing_errors": sum(row["over_under_trigger_error"] for row in executable),
            }
        )
    return out


def failure_taxonomy(rows: list[dict]) -> list[dict]:
    counts: dict[tuple[str, str, str], int] = defaultdict(int)
    for row in rows:
        for failure_class in _failure_classes(row):
            counts[(row["provider"], row["variant"], failure_class)] += 1
    return [
        {
            "provider": provider,
            "variant": variant,
            "failure_class": failure_class,
            "count": count,
        }
        for (provider, variant, failure_class), count in sorted(counts.items())
    ]


def write_category_tex(path: Path, rows: list[dict]) -> None:
    deepseek_rows = [row for row in rows if row["provider"] == "deepseek"]
    lines = [
        "\\begin{tabular}{llrrrr}",
        "\\toprule",
        "Variant & Category & Total & Executed & Success & Routing errors \\\\",
        "\\midrule",
    ]
    for row in deepseek_rows:
        lines.append(
            f"{_tex(str(row['variant']).replace('_', ' '))} & {_tex(str(row['category']).replace('_', ' '))} & "
            f"{row['n_total']} & {row['n_executed']} & {row['success_rate']:.3f} & {row['routing_errors']} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_failure_taxonomy_tex(path: Path, rows: list[dict]) -> None:
    interesting = [row for row in rows if row["provider"] in {"deepseek", "kimi"}]
    lines = [
        "\\begin{tabular}{lllr}",
        "\\toprule",
        "Provider & Variant & Failure class & Count \\\\",
        "\\midrule",
    ]
    for row in interesting:
        lines.append(
            f"{_tex(str(row['provider']))} & {_tex(str(row['variant']).replace('_', ' '))} & "
            f"{_tex(str(row['failure_class']).replace('_', ' '))} & {row['count']} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _failure_classes(row: dict) -> list[str]:
    notes = [str(note) for note in row.get("notes", [])]
    if any(_is_provider_error(note) for note in notes):
        return ["provider_error"]
    if any(_is_parse_error(note) for note in notes):
        return ["parse_error"]
    classes = []
    if row.get("invalid_tool_calls", 0):
        classes.append("invalid_tool_call")
    if row.get("permission_violations", 0):
        classes.append("permission_violation")
    if row.get("unsafe_secret_access", 0):
        classes.append("unsafe_secret_access")
    if row.get("over_under_trigger_error", 0):
        classes.append("routing_error")
    if not row.get("state_diff_correct", False):
        classes.append("state_diff_error")
    if not row.get("task_success", False) and not classes:
        classes.append("other_behavior_failure")
    return classes


def _is_provider_error(note: str) -> bool:
    if not note.startswith("provider_error:"):
        return False
    markers = ("HTTP", "missing environment", "Invalid Authentication", "authentication", "rate limit")
    return any(marker.lower() in note.lower() for marker in markers)


def _is_parse_error(note: str) -> bool:
    if note.startswith("parse_error:"):
        return True
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
