# External Decision Register

This register records the current submission and release defaults. It keeps decisions explicit so later conference-specific packaging can change them without silently changing the manuscript claims.

| Decision | Current status | Selected default in this repository | Unblock action | Affected artifacts |
| --- | --- | --- | --- | --- |
| Venue template | Resolved default | arXiv-style public preprint using the standard LaTeX `article` class. Suggested primary category is `cs.SE`; suggested cross-list is `cs.AI`. | For a later conference submission, adapt `paper/main.tex`, page limits, appendix placement, and workflow to that venue. | `paper/main.tex`, `paper/metadata.json`, `.github/workflows/latex.yml`, `docs/arxiv_submission.md` |
| License | Resolved default | Dual-license release posture: code under MIT; manuscript source, documentation, benchmark cases, evidence snapshots, derived tables, figures, and release metadata under CC BY 4.0. | Revisit only if a target venue, institutional rule, or artifact portal requires different terms. | `LICENSE`, `LICENSE-MIT`, `LICENSE-CC-BY-4.0.md`, `README.md`, `.zenodo.json`, archive bundle |
| Anonymization policy | Resolved default | Non-anonymous preprint with author metadata set to Song Luo. | Prepare a separate anonymized bundle only if a later double-anonymous venue is selected. | `paper/main.tex`, `paper/metadata.json`, `evidence/github_snapshots.md`, `evidence/source_audit.md` |
| Artifact sharing mode | Resolved default | Public Zenodo artifact archive after final inspection; working GitHub repository remains private unless separately opened. | Upload `dist/agent-harness-paper-artifact.zip` and PDF to Zenodo, then record the DOI in release docs. | `docs/artifact_release_index.md`, `docs/zenodo_release_plan.md`, `scripts/build_artifact_archive.py`, generated archive bundle |
| Live-provider rerun policy | Policy fixed | Credentials must be process environment variables only. Committed pilot rows are sufficient for the current preprint. Smoke outputs go to ignored `logs/live-reruns/` paths and are promoted only through `docs/live_rerun_promotion.md`. | Run fresh provider checks only if a reviewer, venue, or release audit requires refreshed rows. | `experiments/run_manifest.md`, `experiments/raw/*.jsonl`, `docs/live_rerun_promotion.md`, result tables |

## Submission Gate

Before any external submission or artifact release, review this register together with `docs/submission_readiness.md`, `docs/artifact_release_index.md`, `docs/arxiv_submission.md`, `docs/zenodo_release_plan.md`, and `docs/final_cleanup.md`. Resolved defaults are enough for the current arXiv-style preprint; later venue-specific releases may impose additional requirements.

## Official References

- arXiv category taxonomy: https://arxiv.org/category_taxonomy
- arXiv endorsement help: https://info.arxiv.org/help/endorsement.html
- Zenodo new upload help: https://help.zenodo.org/docs/deposit/create-new-upload/
- Zenodo license help: https://help.zenodo.org/docs/deposit/describe-records/licenses/
