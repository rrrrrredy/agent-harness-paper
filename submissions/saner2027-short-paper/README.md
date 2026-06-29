# SANER 2027 Short Papers And Posters

## Position

Submit only if the paper is tightened into a software-analysis short paper.

Core framing: agent trajectories are evolving software artifacts. A harness can
analyze state diffs, tool calls, policy violations, replay traces, and
maintenance risk for repository-changing agents.

## Official Constraints

- Format: IEEE conference proceedings format.
- Length: six pages maximum for short papers, including all text, figures,
  references, and appendices.
- Review: double-anonymous; violations can cause desk rejection.
- Abstract submission: mandatory, Monday 19 October 2026.
- Paper deadline: Friday 23 October 2026.
- Submission site: https://easychair.org/my/conference?conf=saner2027

Official page:
https://conf.researchr.org/track/saner-2027/saner-2027-short-papers-and-posters-track

## Paper Conversion

The current preprint must be narrowed:

1. Drop broad agent-product claims.
2. Center on software engineering artifacts: repositories, diffs, tests,
   validation commands, permission policy, and replay logs.
3. Make the contribution a short empirical/tool-oriented result, not only an
   essay.
4. Keep only pilot results that support maintainability and state-diff
   evaluation.
5. Anonymize all author-identifying repository, Zenodo, arXiv, and YouTube
   references.

Repository-fixture evidence:

```powershell
python scripts/run_repo_fixture_demo.py
```

This regenerates:

- `results/fixtures/saner_repo_fixture_summary.md`
- `results/fixtures/saner_repo_fixture_trace.json`
- `results/fixtures/saner_repo_fixture.diff`
- `results/fixtures/saner_repo_fixture_suite.md`
- `results/fixtures/saner_repo_fixture_suite.csv`
- `results/fixtures/saner_repo_fixture_suite.json`

The fixture maps benchmark case `state_002` to a concrete before/after
repository tree, a unified diff, a trace with file hashes, and a no-dependency
test result. The suite also includes negative scenarios for missing tests,
wrong-file mutation, and secret-boundary access.

## Anonymization Plan

- Replace public links with `Anonymous supplemental artifact`.
- Remove author name and email.
- Rename project references that identify ownership.
- Do not include YouTube or GitHub links in the submitted PDF.
- Provide a zip through EasyChair additional materials if possible.

## Anonymous Supplemental Package

Build a local anonymous package with:

```powershell
python scripts/build_anonymous_submission_artifact.py --track saner2027-short-paper
python scripts/check_anonymous_submission_package.py --track saner2027-short-paper --build --run-smoke
```

Output:

- `dist/anonymous/saner2027-short-paper-anonymous-artifact.zip`

The package includes the harness, benchmark cases, selected recorded rows,
regenerated result tables, the repository fixture suite, and the anonymous
SANER Short Paper source. The independent checker verifies required files,
forbidden path classes, unsafe zip paths, author-identifying strings, the
reviewer smoke path, and repository-fixture regeneration.
