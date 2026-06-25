# Reproducibility

## Local Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip pytest
.\.venv\Scripts\python -m pytest
```

## Deterministic Artifacts

```powershell
.\.venv\Scripts\python scripts\run_codex_reference.py
.\.venv\Scripts\python scripts\analyze_results.py
.\.venv\Scripts\python scripts\generate_figures.py
.\.venv\Scripts\python scripts\secret_scan.py
```

## Live Artifacts

Live model execution requires valid provider credentials in the process environment. Missing or invalid credentials should be reported as provider failures and must not be substituted with invented numbers.

## Paper

The LaTeX source is in `paper/main.tex`. If `pdflatex` and `bibtex` are installed:

```powershell
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

If no TeX distribution is installed, source-level checks and bibliography review are the available validation layer.
