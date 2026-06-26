from __future__ import annotations

import csv
import json
import math
import random
from collections import defaultdict
from pathlib import Path


RAW = Path("experiments/raw")
OUT = Path("results/tables")
LIVE_PROVIDERS = {"deepseek", "kimi"}
BOOTSTRAP_SEED = 20260626
BOOTSTRAP_SAMPLES = 10_000


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    rows = [row for row in load_rows() if row.get("provider") in LIVE_PROVIDERS]
    uncertainty_rows = build_uncertainty_rows(rows)
    pairwise_rows = build_pairwise_rows(rows)

    write_csv(OUT / "live_success_uncertainty.csv", uncertainty_rows)
    write_md(OUT / "live_success_uncertainty.md", uncertainty_rows)
    write_uncertainty_tex(OUT / "live_success_uncertainty.tex", uncertainty_rows)

    write_csv(OUT / "live_pairwise_delta.csv", pairwise_rows)
    write_md(OUT / "live_pairwise_delta.md", pairwise_rows)
    write_pairwise_tex(OUT / "live_pairwise_delta.tex", pairwise_rows)
    print(f"wrote live uncertainty tables for {len(rows)} rows")


def load_rows() -> list[dict]:
    rows: list[dict] = []
    for path in sorted(RAW.glob("*.jsonl")):
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                if line.strip():
                    rows.append(json.loads(line))
    return rows


def build_uncertainty_rows(rows: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[(row["provider"], row["variant"])].append(row)

    out: list[dict] = []
    for (provider, variant), items in sorted(grouped.items()):
        executed = [row for row in items if not is_provider_error(row)]
        n = len(executed)
        task_successes = sum(1 for row in executed if row.get("task_success", False))
        state_successes = sum(1 for row in executed if row.get("state_diff_correct", False))
        task_low, task_high = wilson_interval(task_successes, n)
        state_low, state_high = wilson_interval(state_successes, n)
        out.append(
            {
                "provider": provider,
                "variant": variant,
                "n_executed": n,
                "task_successes": task_successes,
                "task_success_rate": fmt_rate(task_successes, n),
                "task_success_ci95": fmt_interval(task_low, task_high),
                "state_diff_successes": state_successes,
                "state_diff_rate": fmt_rate(state_successes, n),
                "state_diff_ci95": fmt_interval(state_low, state_high),
            }
        )
    return out


def build_pairwise_rows(rows: list[dict]) -> list[dict]:
    by_provider: dict[str, dict[tuple[str, str], dict]] = defaultdict(dict)
    for row in rows:
        if is_provider_error(row):
            continue
        by_provider[row["provider"]][(row["variant"], row["case_id"])] = row

    out: list[dict] = []
    for provider, provider_rows in sorted(by_provider.items()):
        paired = []
        case_ids = sorted(
            case_id
            for variant, case_id in provider_rows
            if variant == "thin_contract" and ("thick_checklist", case_id) in provider_rows
        )
        for case_id in case_ids:
            thin = provider_rows[("thin_contract", case_id)]
            thick = provider_rows[("thick_checklist", case_id)]
            paired.append(
                (
                    1 if thin.get("task_success", False) else 0,
                    1 if thick.get("task_success", False) else 0,
                )
            )
        deltas = [thin - thick for thin, thick in paired]
        low, high = paired_bootstrap_ci(deltas)
        out.append(
            {
                "provider": provider,
                "comparison": "thin_contract - thick_checklist",
                "n_paired_cases": len(paired),
                "paired_delta": fmt_number(mean(deltas)),
                "bootstrap_ci95": fmt_interval(low, high),
                "thin_only_wins": sum(1 for thin, thick in paired if thin == 1 and thick == 0),
                "thick_only_wins": sum(1 for thin, thick in paired if thin == 0 and thick == 1),
                "both_success": sum(1 for thin, thick in paired if thin == 1 and thick == 1),
                "both_fail": sum(1 for thin, thick in paired if thin == 0 and thick == 0),
            }
        )
    return out


def wilson_interval(successes: int, n: int, z: float = 1.959963984540054) -> tuple[float, float]:
    if n == 0:
        return (0.0, 0.0)
    phat = successes / n
    denom = 1 + z * z / n
    center = (phat + z * z / (2 * n)) / denom
    half = z * math.sqrt((phat * (1 - phat) + z * z / (4 * n)) / n) / denom
    return (max(0.0, center - half), min(1.0, center + half))


def paired_bootstrap_ci(deltas: list[int]) -> tuple[float, float]:
    if not deltas:
        return (0.0, 0.0)
    rng = random.Random(BOOTSTRAP_SEED)
    samples = []
    n = len(deltas)
    for _ in range(BOOTSTRAP_SAMPLES):
        draw = [deltas[rng.randrange(n)] for _ in range(n)]
        samples.append(mean(draw))
    samples.sort()
    low_idx = int(0.025 * (len(samples) - 1))
    high_idx = int(0.975 * (len(samples) - 1))
    return samples[low_idx], samples[high_idx]


def mean(values: list[int]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def is_provider_error(row: dict) -> bool:
    for note in row.get("notes", []):
        text = str(note).lower()
        if text.startswith("provider_error:") and any(
            marker in text for marker in ("http", "authentication", "missing environment", "rate limit")
        ):
            return True
    return False


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
        path.write_text("No rows found.\n", encoding="utf-8")
        return
    headers = list(rows[0])
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row[h]) for h in headers) + " |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_uncertainty_tex(path: Path, rows: list[dict]) -> None:
    lines = [
        "\\begin{tabular}{llrll}",
        "\\toprule",
        "Provider & Variant & N & Success (95\\% CI) & State diff (95\\% CI) \\\\",
        "\\midrule",
    ]
    for row in rows:
        success = f"{row['task_success_rate']} ({row['task_success_ci95']})"
        state = f"{row['state_diff_rate']} ({row['state_diff_ci95']})"
        lines.append(
            f"{tex(row['provider'])} & {tex(str(row['variant']).replace('_', ' '))} & "
            f"{row['n_executed']} & {tex(success)} & {tex(state)} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_pairwise_tex(path: Path, rows: list[dict]) -> None:
    lines = [
        "\\begin{tabular}{lrrrll}",
        "\\toprule",
        "Provider & N & Delta & Thin-only & Thick-only & Bootstrap 95\\% CI \\\\",
        "\\midrule",
    ]
    for row in rows:
        lines.append(
            f"{tex(row['provider'])} & {row['n_paired_cases']} & {row['paired_delta']} & "
            f"{row['thin_only_wins']} & {row['thick_only_wins']} & {tex(row['bootstrap_ci95'])} \\\\"
        )
    lines.extend(["\\bottomrule", "\\end{tabular}"])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def fmt_rate(successes: int, n: int) -> str:
    if n == 0:
        return "0.000"
    return fmt_number(successes / n)


def fmt_number(value: float) -> str:
    return f"{value:.3f}"


def fmt_interval(low: float, high: float) -> str:
    return f"[{low:.3f}, {high:.3f}]"


def tex(value: object) -> str:
    return str(value).replace("_", "\\_").replace("&", "\\&").replace("%", "\\%")


if __name__ == "__main__":
    main()
