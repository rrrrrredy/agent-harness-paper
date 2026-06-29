# Submission Status

Last updated: 2026-06-29.

## Active Routes

| Route | Current PDF pages | Limit posture | Artifact mode | Current state |
|---|---:|---|---|---|
| ICSE 2027 NIER | 3 | 4 pages main text plus 1 references-only page | Anonymous supplemental zip | Draft expanded and CI-compiled |
| SANER 2027 Tool Demo | 3 | 5 pages including references | Public GitHub, Zenodo, GitHub Release screencast | Primary route draft expanded and CI-compiled |
| SANER 2027 Short Paper | 3 | 6 pages including references | Anonymous supplemental zip | Draft expanded with repository fixture suite evidence |

## Latest Checks

- Local validation: `python scripts/run_checks.py --mode validate` passed after
  SANER package-builder and anonymous-package checker expansion.
- GitHub Actions validate run: `28354603340` passed.
- GitHub Actions PDF run: `28354603363` passed.
- Latest PDFs downloaded under `logs/submission-pdfs/`.
- Repository fixture suite regenerated under `results/fixtures/`.
- ICSE NIER anonymous artifact rebuilt at
  `dist/anonymous/icse2027-nier-anonymous-artifact.zip`.
- ICSE NIER anonymous artifact passed
  `python scripts/check_anonymous_submission_package.py --track icse2027-nier --build --run-smoke`.
- SANER Short Paper anonymous artifact rebuilt at
  `dist/anonymous/saner2027-short-paper-anonymous-artifact.zip`.
- SANER Short Paper anonymous artifact passed
  `python scripts/check_anonymous_submission_package.py --track saner2027-short-paper --build --run-smoke`.
- SANER repository fixture suite regenerated under `results/fixtures/` with
  success, missing-test, wrong-file, and secret-read scenarios.
- Anonymous package smoke test passed with `python scripts/smoke_test.py`.
- Anonymous package walkthrough passed with `python scripts/run_demo_walkthrough.py`.
- SANER Tool Demo local submission index can be regenerated with
  `python scripts/build_saner_tool_demo_package.py`.
- Final sub-agent adversarial review fixes are recorded in
  `submissions/reviews/adversarial_review_summary.md`.

## Removed Route

The YouTube-required tool-demo route has been removed from the active plan and
from tracked repository files. The release keeps only the SANER screencast
asset.

## Next Work

- Before uploading ICSE NIER or SANER Short Paper, rerun the matching anonymous
  package checker with `--build --run-smoke`.
- Treat SANER Tool Demo as the primary conference target unless a later review
  exposes a stronger route.
- Keep SANER Short Paper claims narrow unless more repository fixtures or
  failure cases are added.
