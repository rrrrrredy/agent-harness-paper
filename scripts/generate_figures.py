from __future__ import annotations

import csv
from pathlib import Path


SUMMARY = Path("results/tables/experiment_summary.csv")
OUT = Path("figures/success_by_variant.svg")


def main() -> None:
    if not SUMMARY.exists():
        raise SystemExit("missing results/tables/experiment_summary.csv; run analyze_results.py first")
    rows = list(csv.DictReader(SUMMARY.open("r", encoding="utf-8")))
    width = 760
    height = 260
    margin = 50
    bar_w = 42
    gap = 18
    x = margin
    bars = []
    labels = []
    for row in rows:
        value = float(row["task_success_rate"])
        bar_h = int(value * 160)
        y = height - margin - bar_h
        bars.append(f'<rect x="{x}" y="{y}" width="{bar_w}" height="{bar_h}" fill="#2f6f73" />')
        bars.append(f'<text x="{x + bar_w / 2}" y="{y - 6}" text-anchor="middle" font-size="11">{value:.2f}</text>')
        label = f'{row["provider"]}\\n{row["variant"]}'
        labels.append(f'<text x="{x + bar_w / 2}" y="{height - 34}" text-anchor="middle" font-size="9">{label}</text>')
        x += bar_w + gap
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" fill="white"/>
<text x="{margin}" y="25" font-size="16" font-family="Arial">Task success rate by provider and harness variant</text>
<line x1="{margin}" y1="{height - margin}" x2="{width - margin}" y2="{height - margin}" stroke="#222"/>
<line x1="{margin}" y1="{height - margin - 160}" x2="{width - margin}" y2="{height - margin - 160}" stroke="#ddd"/>
{''.join(bars)}
{''.join(labels)}
</svg>
'''
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
