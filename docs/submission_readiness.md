# Submission Readiness Checklist

This checklist records the current submission-ready preprint posture and separates it from later venue-specific changes.

## Artifact-Ready Checks

- Manuscript source exists at `paper/main.tex`.
- Bibliography exists at `paper/references.bib` and passes `scripts/check_tex_sources.py`.
- Venue-neutral metadata exists at `paper/metadata.json`.
- Result tables and figure regenerate from committed raw results with `python scripts/run_checks.py --mode regenerate`.
- Validation passes with `python scripts/run_checks.py --mode validate`.
- PDF build workflow exists at `.github/workflows/latex.yml`.
- Validation workflow exists at `.github/workflows/validate.yml`.
- PDF artifact retrieval is documented in `docs/artifact_release_index.md` and `docs/reproducibility.md`.
- Claim boundaries are documented in `docs/claim_boundaries.md`.
- External release and venue decisions are tracked in `docs/external_decision_register.md`.
- Experiment protocol and run manifest are documented in `docs/experiment_protocol.md` and `experiments/run_manifest.md`.
- Evidence artifacts are documented in `evidence/github_snapshots.md` and `evidence/source_audit.md`.
- Public-trace, release-reference, entrypoint-command, artifact-consistency, and secret-scan checks are included in validation.
- Dual-license files exist: `LICENSE`, `LICENSE-MIT`, and `LICENSE-CC-BY-4.0.md`.
- Citation and Zenodo metadata exist: `CITATION.cff` and `.zenodo.json`.

## Selected Submission Defaults

- Target: arXiv-style public preprint before any conference-specific submission.
- Template: standard LaTeX `article` class, kept arXiv-friendly and not adapted to a proceedings format.
- Author metadata: non-anonymous, `Song Luo`.
- Suggested arXiv category: primary `cs.SE`, cross-list `cs.AI` if accepted by arXiv moderation.
- License: code under MIT; manuscript source, documentation, benchmark cases, evidence snapshots, derived tables, figures, and release metadata under CC BY 4.0.
- Artifact sharing: public Zenodo archive DOI `10.5281/zenodo.20907471`; private GitHub repository remains private unless separately opened.
- Live-provider reruns: committed pilot logs are sufficient for the current preprint; any fresh rerun must go through `docs/live_rerun_promotion.md`.

These decisions are summarized in `docs/external_decision_register.md`. Later conference submission may still require a separate template, page-limit pass, or anonymized bundle.

## Pre-Submission Sequence

1. Run `python scripts/run_checks.py --mode regenerate`.
2. Run `python scripts/run_checks.py --mode validate`.
3. Build or download the PDF artifact.
4. Confirm author information, acknowledgement text, and arXiv category selection.
5. Confirm no credential, private path, or process-trace terms appear in public-facing files.
6. Review `docs/external_decision_register.md`, `docs/arxiv_submission.md`, and `docs/zenodo_release_plan.md`.
7. Run `python scripts/build_artifact_archive.py --check`.
8. Build `dist/agent-harness-paper-artifact.zip` with `python scripts/build_artifact_archive.py`.
