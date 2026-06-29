# SANER 2027 Tool Demo Submission Package

## Primary Files

- Paper source: `submissions/saner2027-tool-demo/paper/main.tex`
- Latest CI PDF: `logs/submission-pdfs/saner2027-tool-demo/paper/main.pdf`
- Public tool repository: https://github.com/rrrrrredy/agent-harness-paper
- Public archive: https://doi.org/10.5281/zenodo.20907471
- Screencast: https://github.com/rrrrrredy/agent-harness-paper/releases/download/v0.1.0-preprint/agent-harness-saner-tool-demo-video.mp4
- Release page: https://github.com/rrrrrredy/agent-harness-paper/releases/tag/v0.1.0-preprint

## Submission Metadata

- Track: Tool Demo Track.
- Review model: single-anonymous; author identity is allowed.
- Author: Song Luo.
- Title: `Replayable State-Diff Harnesses for Repository-Changing Agents`.
- Tool URL: `https://github.com/rrrrrredy/agent-harness-paper`.
- Optional video URL: GitHub Release screencast above.
- Artifact DOI: `10.5281/zenodo.20907471`.

## Reviewer Commands

```powershell
python scripts/run_checks.py --mode validate
python scripts/run_demo_walkthrough.py
python scripts/run_repo_fixture_demo.py
```

Expected inspection points:

- `results/fixtures/saner_repo_fixture.diff`
- `results/fixtures/saner_repo_fixture_suite.md`
- `results/tables/failure_taxonomy.md`
- `results/tables/experiment_summary.md`

## Current CI Evidence

- Validate workflow: `28352621244`
- PDF workflow: `28352621207`
- Current PDF page count: 3 pages.

## Final Pre-Submit Checklist

- Rebuild PDF from the final branch or download the latest CI artifact.
- Confirm the PDF still includes repository, archive, and screencast URLs.
- Confirm the GitHub repository is public.
- Confirm the release asset video opens without authentication.
- Confirm `python scripts/run_checks.py --mode validate` passes.
- Confirm no API keys or private endorsement links are present.
