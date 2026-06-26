# Reproducibility

## Local Setup

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip pytest
.\.venv\Scripts\python -m pytest
```

## Single-Command Routines

```powershell
python scripts\run_checks.py --mode validate
python scripts\run_checks.py --mode regenerate
```

## Deterministic Artifacts

```powershell
.\.venv\Scripts\python scripts\run_local_reference.py
.\.venv\Scripts\python scripts\backfill_run_metadata.py
.\.venv\Scripts\python scripts\analyze_results.py
.\.venv\Scripts\python scripts\generate_figures.py
.\.venv\Scripts\python scripts\check_tex_sources.py
.\.venv\Scripts\python scripts\check_public_traces.py
.\.venv\Scripts\python scripts\secret_scan.py
```

## Live Artifacts

Live model execution requires valid provider credentials in the process environment. Missing or invalid credentials should be reported as provider failures and must not be substituted with invented numbers.

Credential preflight checks only whether the required environment variable is present; they do not print credential values.

```powershell
.\.venv\Scripts\python scripts\check_provider_credentials.py --provider deepseek
.\.venv\Scripts\python scripts\check_provider_credentials.py --provider kimi
```

Use ignored `logs\live-reruns\` outputs for new provider smoke tests. The live runner refuses to overwrite an existing output unless `--resume` or `--force-overwrite` is supplied.
Promote smoke outputs into cited raw results only through `docs/live_rerun_promotion.md`.

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
gh run download 28214303513 -n agent-harness-paper-pdf -D logs\artifact-download
Get-Item logs\artifact-download\main.pdf
```

`logs/` is ignored by git. Remove the temporary download directory after inspection.

## Archive Bundle

The archive helper packages tracked source artifacts and excludes local state, logs, virtual environments, secrets, generated PDFs, and download leftovers.

```powershell
python scripts\build_artifact_archive.py --check
python scripts\check_archive_manifest_alignment.py
python scripts\build_artifact_archive.py
```

The default zip output is `dist/agent-harness-paper-artifact.zip`; `dist/` is ignored by git.

Before sharing the archive externally, review `docs/external_decision_register.md` for venue template, license, anonymization, artifact-sharing, and live-provider rerun decisions that are intentionally outside deterministic regeneration.
