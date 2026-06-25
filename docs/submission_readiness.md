# Submission Readiness Checklist

This checklist separates repository artifact readiness from venue-specific submission work.

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
- Experiment protocol and run manifest are documented in `docs/experiment_protocol.md` and `experiments/run_manifest.md`.
- Evidence artifacts are documented in `evidence/github_snapshots.md` and `evidence/source_audit.md`.
- Public-trace, release-reference, entrypoint-command, artifact-consistency, and secret-scan checks are included in validation.

## Venue-Specific Decisions

- Submission target and template.
- Page limit and appendix policy.
- Anonymous versus non-anonymous author metadata.
- PDF upload format and whether supplementary artifacts are accepted as a repository link, zip, or archival bundle.
- License statement for code, benchmark cases, and manuscript source. No repository-wide license has been selected yet.
- Artifact review expectations, including whether network-dependent GitHub evidence refreshes are allowed.
- Whether live-provider reruns are expected or the committed pilot logs are sufficient.

## Pre-Submission Sequence

1. Select the venue and copy or adapt its required template.
2. Run `python scripts/run_checks.py --mode regenerate`.
3. Run `python scripts/run_checks.py --mode validate`.
4. Build or download the PDF artifact.
5. Confirm venue-specific metadata, author information, and acknowledgements.
6. Confirm no credential, private path, or process-trace terms appear in public-facing files.
7. Archive the artifact package in the format requested by the venue.
