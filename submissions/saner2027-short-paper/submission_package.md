# SANER 2027 Short Paper Submission Package

## Primary Files

- Paper source: `submissions/saner2027-short-paper/paper/main.tex`
- Latest CI PDF: `logs/submission-pdfs/saner2027-short-paper/paper/main.pdf`
- Anonymous supplemental artifact:
  `dist/anonymous/saner2027-short-paper-anonymous-artifact.zip`

## Submission Metadata

- Track: Short Papers and Posters.
- Review model: double-anonymous.
- Author field in submitted PDF: `Anonymous Author(s)`.
- Title: `Evaluating Repository-Changing Agents Through State-Diff Contracts`.
- Artifact mode: anonymous supplemental zip.

## Package Commands

```powershell
python scripts/build_anonymous_submission_artifact.py --track saner2027-short-paper
python scripts/check_anonymous_submission_package.py --track saner2027-short-paper --build --run-smoke
```

The checker verifies required files, forbidden path classes, author-identifying
strings, unsafe zip paths, the no-dependency reviewer walkthrough, and the
repository-fixture regeneration path.

## Current CI Evidence

- PDF workflow: `28353360782`
- Validate workflow: `28353360786`
- Current PDF page count: 3 pages.

## Final Pre-Submit Checklist

- Confirm the PDF has no author name, public repository URL, Zenodo DOI, arXiv
  endorsement link, or acknowledgments.
- Confirm the argument stays within short-paper scope: state diffs, repository
  mutation, tests, traces, and maintenance risk.
- Rebuild the anonymous supplemental artifact with the commands above.
- Upload only the anonymous zip as supplemental material if EasyChair permits
  additional artifacts.
- Keep the abstract-submission and full-paper deadlines in the calendar before
  opening the final EasyChair submission.
