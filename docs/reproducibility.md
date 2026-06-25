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
.\.venv\Scripts\python scripts\backfill_run_metadata.py
.\.venv\Scripts\python scripts\analyze_results.py
.\.venv\Scripts\python scripts\generate_figures.py
.\.venv\Scripts\python scripts\check_tex_sources.py
.\.venv\Scripts\python scripts\check_public_traces.py
.\.venv\Scripts\python scripts\secret_scan.py
```

## Live Artifacts

Live model execution requires valid provider credentials in the process environment. Missing or invalid credentials should be reported as provider failures and must not be substituted with invented numbers.

Parser-instrumentation repair for already recorded live rows also requires the relevant provider credential:

```powershell
.\.venv\Scripts\python scripts\rerun_parse_errors.py --provider deepseek
```

## GitHub Evidence Snapshot

The GitHub evidence snapshot is reproducible but not deterministic: it uses `gh`, current repository metadata, PR metadata, and a generation timestamp. Regenerate it only when intentionally refreshing the evidence layer.

```powershell
.\.venv\Scripts\python scripts\collect_github_evidence.py
.\.venv\Scripts\python scripts\audit_source_evidence.py
```

For routine validation without network calls, rebuild the source-audit markdown from the committed JSON snapshot:

```powershell
.\.venv\Scripts\python scripts\audit_source_evidence.py --offline
```

## Paper

The LaTeX source is in `paper/main.tex`. If `pdflatex` and `bibtex` are installed:

```powershell
Push-Location paper
pdflatex -interaction=nonstopmode main.tex
bibtex main
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
Pop-Location
```

If no TeX distribution is installed, source-level checks and bibliography review are the available validation layer.

The repository also includes `.github/workflows/latex.yml`, which builds `paper/main.pdf` on GitHub Actions and uploads it as an artifact. This avoids requiring a local TeX installation on Windows.

To retrieve a checked PDF artifact from the current repository checkout:

```powershell
New-Item -ItemType Directory -Force logs\artifact-download | Out-Null
gh run download 28164140135 -n agent-harness-paper-pdf -D logs\artifact-download
Get-Item logs\artifact-download\main.pdf
```

`logs/` is ignored by git. Remove the temporary download directory after inspection.
