# ICSE 2027 NIER Submission Package

## Primary Files

- Paper source: `submissions/icse2027-nier/paper/main.tex`
- Latest CI PDF: `logs/submission-pdfs/icse2027-nier/paper/main.pdf`
- Anonymous supplemental artifact:
  `dist/anonymous/icse2027-nier-anonymous-artifact.zip`

## Submission Metadata

- Track: New Ideas and Emerging Results.
- Review model: double-anonymous.
- Author field in submitted PDF: `Anonymous Author(s)`.
- Title: `Thin Harnesses as System-Boundary Contracts for Stateful AI Agents`.
- Artifact mode: anonymous supplemental zip, not public GitHub/Zenodo links.

## Package Commands

```powershell
python scripts/build_anonymous_submission_artifact.py --track icse2027-nier
python scripts/check_anonymous_submission_package.py --track icse2027-nier --build --run-smoke
```

The checker verifies required files, forbidden path classes, author-identifying
strings, unsafe zip paths, and the no-dependency reviewer walkthrough.

## Current CI Evidence

- PDF workflow: `28352621207`
- Validate workflow: `28352769162`
- Current PDF page count: 3 pages.

## Final Pre-Submit Checklist

- Confirm the PDF has no author name, public repository URL, Zenodo DOI, arXiv
  endorsement link, or acknowledgments.
- Confirm the paper includes a section titled `Future Plans`.
- Rebuild the anonymous supplemental artifact with the commands above.
- Upload only the anonymous zip as supplemental material.
- Do not include public release, GitHub, YouTube, or Zenodo links in the
  double-anonymous submission form unless the venue explicitly provides a
  non-identifying artifact mechanism.
