# Submission Status

Last updated: 2026-06-29.

## Active Routes

| Route | Current PDF pages | Limit posture | Artifact mode | Current state |
|---|---:|---|---|---|
| ICSE 2027 NIER | 3 | 4 pages main text plus 1 references-only page | Anonymous supplemental zip | Draft expanded and CI-compiled |
| SANER 2027 Tool Demo | 2 | 5 pages including references | Public GitHub, Zenodo, GitHub Release screencast | Draft expanded and CI-compiled |
| SANER 2027 Short Paper | 3 | 6 pages including references | Anonymous package preferred | Draft expanded with repository fixture evidence |

## Latest Checks

- Local validation: `python scripts/run_checks.py --mode validate` passed after
  active-route expansion.
- GitHub Actions PDF run: `28348467190` passed.
- Latest PDFs downloaded under `logs/submission-pdfs/`.
- ICSE NIER anonymous artifact rebuilt at
  `dist/anonymous/icse2027-nier-anonymous-artifact.zip`.
- Anonymous package smoke test passed with `python scripts/smoke_test.py`.
- Anonymous package walkthrough passed with `python scripts/run_demo_walkthrough.py`.

## Removed Route

The YouTube-required tool-demo route has been removed from the active plan and
from tracked repository files. The release keeps only the SANER screencast
asset.

## Next Work

- Tighten ICSE NIER to exactly match the final double-anonymous submission
  instructions before uploading.
- Decide whether SANER Tool Demo should be the primary conference target.
- Expand SANER Short Paper only if adding more repository fixtures or failure
  cases is feasible; keep claims narrow otherwise.
