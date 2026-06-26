# Artifact Release Index

This index provides a compact entrypoint for reviewing, rebuilding, and validating the artifact package.

## Status And License

This is a submission-ready, non-anonymous arXiv-style preprint artifact package for Song Luo. It uses the standard LaTeX `article` class rather than a conference proceedings template. The intended release posture is a public Zenodo artifact archive while the working GitHub repository remains private unless separately opened.

The repository is dual-licensed. Code is under the MIT License; the manuscript source, documentation, benchmark cases, evidence snapshots, derived tables, figures, and release metadata are under Creative Commons Attribution 4.0 International (CC BY 4.0). See `LICENSE`, `LICENSE-MIT`, and `LICENSE-CC-BY-4.0.md`.
Submission, license, anonymization, artifact-sharing, and live-provider rerun decisions are tracked in `docs/external_decision_register.md`.

## Manuscript

- Source: `paper/main.tex`
- Bibliography: `paper/references.bib`
- Metadata: `paper/metadata.json`
- PDF build workflow: `.github/workflows/latex.yml`
- Latest checked PDF run: `28216768495`
- PDF artifact name: `agent-harness-paper-pdf`

To retrieve the checked PDF artifact with GitHub CLI:

```powershell
gh run download 28216768495 -n agent-harness-paper-pdf -D logs\artifact-download
```

`logs/` is ignored by git and can be removed after local inspection.

## Validation

- Local validation command: `python scripts/run_checks.py --mode validate`
- Regeneration command: `python scripts/run_checks.py --mode regenerate`
- Validation workflow: `.github/workflows/validate.yml`
- Current validation status: `gh run list --workflow "Validate artifact package" --limit 1`

Validation covers deterministic tests, citation/source checks, public-trace checks, artifact consistency, external-decision register checks, archive-manifest alignment, offline source-audit validation, and secret scanning.

## Evidence And Results

- Artifact map: `artifact_manifest.json`
- Reviewer guide: `docs/reviewer_guide.md`
- Claim traceability: `docs/claim_traceability.md`
- Claim boundaries: `docs/claim_boundaries.md`
- External decision register: `docs/external_decision_register.md`
- arXiv submission notes: `docs/arxiv_submission.md`
- Zenodo release plan: `docs/zenodo_release_plan.md`
- Data dictionary: `docs/data_dictionary.md`
- Live rerun promotion: `docs/live_rerun_promotion.md`
- Experiment protocol: `docs/experiment_protocol.md`
- Run manifest: `experiments/run_manifest.md`
- GitHub evidence snapshot: `evidence/github_snapshots.md`
- Source audit: `evidence/source_audit.md`
- Result summary: `results/tables/experiment_summary.md`
- Category summary: `results/tables/category_summary.md`
- Failure taxonomy: `results/tables/failure_taxonomy.md`
- Live uncertainty: `results/tables/live_success_uncertainty.md`
- Live paired delta: `results/tables/live_pairwise_delta.md`
- Figure: `figures/success_by_variant.svg`

## Rebuild Order

1. Run `python scripts/run_checks.py --mode regenerate`.
2. Run `python scripts/run_checks.py --mode validate`.
3. Trigger or inspect `.github/workflows/latex.yml` for the PDF artifact.
4. Compare manuscript claims against `docs/claim_boundaries.md`, `experiments/run_manifest.md`, and regenerated result tables.
