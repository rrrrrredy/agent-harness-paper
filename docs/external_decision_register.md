# External Decision Register

This register keeps venue, release, and reviewer-dependent choices outside the manuscript and deterministic artifact checks. The repository remains venue-neutral until these decisions are made for a specific submission or external artifact release.

| Decision | Current status | Safe default in this repository | Unblock action | Affected artifacts |
| --- | --- | --- | --- | --- |
| Venue template | External decision required | Keep `paper/main.tex` and `paper/metadata.json` venue-neutral. Do not assume page limits, appendix placement, or proceedings macros. | Select the target venue and adapt the LaTeX source, metadata, and PDF workflow to its template. | `paper/main.tex`, `paper/metadata.json`, `.github/workflows/latex.yml` |
| License | External decision required | No repository-wide license is selected. Treat the package as private review material until reuse terms are chosen. | Choose separate or unified terms for manuscript source, benchmark cases, scripts, and generated artifacts before external release. | `README.md`, `docs/artifact_release_index.md`, archive bundle, release notes |
| Anonymization policy | External decision required | Keep the private artifact package internally consistent and do not create a partially anonymized public bundle. | If the venue is double-anonymous, prepare a separate anonymized submission bundle and decide how to replace direct owner/repository evidence without weakening claim boundaries. | `paper/main.tex`, `paper/metadata.json`, `evidence/github_snapshots.md`, `evidence/source_audit.md` |
| Artifact sharing mode | External decision required | Use the private repository as the working artifact and create `dist/agent-harness-paper-artifact.zip` only when a reviewer or venue requests a zip. | Decide whether reviewers receive a private repository link, a zip bundle, an archival DOI, or a venue artifact portal upload. | `docs/artifact_release_index.md`, `scripts/build_artifact_archive.py`, generated archive bundle |
| Live-provider rerun policy | Policy fixed; execution decision external | Credentials must be process environment variables only. Smoke outputs go to ignored `logs/live-reruns/` paths and are promoted only through `docs/live_rerun_promotion.md`. | Decide whether fresh provider reruns are required for the submission or whether committed pilot rows are sufficient. | `experiments/run_manifest.md`, `experiments/raw/*.jsonl`, `docs/live_rerun_promotion.md`, result tables |

## Submission Gate

Before any external submission or artifact release, this register should be reviewed together with `docs/submission_readiness.md`, `docs/artifact_release_index.md`, and `docs/final_cleanup.md`. Unresolved rows are acceptable for the private working repository, but not for a venue-specific release package.
