# Artifact Release Index

This index provides a compact entrypoint for reviewing, rebuilding, and validating the artifact package.

## Status And License

This is a working preprint artifact package, not a venue-specific submission bundle. No repository-wide license has been selected yet; reuse terms should be decided before external artifact release.

## Manuscript

- Source: `paper/main.tex`
- Bibliography: `paper/references.bib`
- Metadata: `paper/metadata.json`
- PDF build workflow: `.github/workflows/latex.yml`
- Latest checked PDF run: `28164140135`
- PDF artifact name: `agent-harness-paper-pdf`

To retrieve the checked PDF artifact with GitHub CLI:

```powershell
gh run download 28164140135 -n agent-harness-paper-pdf -D logs\artifact-download
```

`logs/` is ignored by git and can be removed after local inspection.

## Validation

- Local validation command: `python scripts/run_checks.py --mode validate`
- Regeneration command: `python scripts/run_checks.py --mode regenerate`
- Validation workflow: `.github/workflows/validate.yml`
- Current validation status: `gh run list --workflow "Validate artifact package" --limit 1`

Validation covers deterministic tests, citation/source checks, public-trace checks, artifact consistency, offline source-audit validation, and secret scanning.

## Evidence And Results

- Artifact map: `artifact_manifest.json`
- Reviewer guide: `docs/reviewer_guide.md`
- Claim boundaries: `docs/claim_boundaries.md`
- Experiment protocol: `docs/experiment_protocol.md`
- Run manifest: `experiments/run_manifest.md`
- GitHub evidence snapshot: `evidence/github_snapshots.md`
- Source audit: `evidence/source_audit.md`
- Result summary: `results/tables/experiment_summary.md`
- Category summary: `results/tables/category_summary.md`
- Failure taxonomy: `results/tables/failure_taxonomy.md`
- Figure: `figures/success_by_variant.svg`

## Rebuild Order

1. Run `python scripts/run_checks.py --mode regenerate`.
2. Run `python scripts/run_checks.py --mode validate`.
3. Trigger or inspect `.github/workflows/latex.yml` for the PDF artifact.
4. Compare manuscript claims against `docs/claim_boundaries.md`, `experiments/run_manifest.md`, and regenerated result tables.
