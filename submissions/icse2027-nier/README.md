# ICSE 2027 NIER

## Position

Submit as a new-ideas paper, not as a conventional empirical paper.

Core idea: capability-patch harnesses become technical debt as models improve,
while system-boundary harnesses become infrastructure. The paper should argue
for a research agenda around thin agent harnesses with strong contracts for
state, tools, permissions, memory, replay, audit, and review.

## Official Constraints

- Track: New Ideas and Emerging Results.
- Length: four pages of main text plus one references-only page.
- Review: double-anonymous.
- Required structure: include a section titled `Future Plans`.
- Submission must not identify the author in paper text, repository links,
  acknowledgments, self-citations, video links, or artifact metadata.
- Target version must be self-contained and should not rely on a public personal
  GitHub repository for review.
- Official page:
  https://conf.researchr.org/track/icse-2027/icse-2027-new-ideas-and-emerging-results--nier-

## Paper Conversion

The NIER version should not look like a weak full paper. It should:

1. Open with the conceptual conflict: harnesses as debt vs harnesses as
   infrastructure.
2. Define two harness classes: capability patches and system-boundary contracts.
3. Present the first-principles argument that external side effects require
   durable contracts regardless of model progress.
4. Use the 24-case pilot only as feasibility evidence.
5. End with `Future Plans`: enforceable contracts, replayable traces,
   state-diff oracles, permission policy, memory scoping, and human review.

## Anonymization Plan

- Replace author with `Anonymous Author(s)`.
- Replace GitHub and Zenodo links with `Anonymous artifact package, submitted as
  supplemental material`.
- Rename first-party project examples to neutral labels such as SkillOps-style
  skill lifecycle, radar-style publication workflow, scheduler PR example, and
  memory-recall PR example.
- Convert first-person ownership claims to artifact-based descriptions.
- Remove email, profile, arXiv, Zenodo, and YouTube references.

## Anonymous Supplemental Package

Build a local anonymous package with:

```powershell
python scripts/build_anonymous_submission_artifact.py --track icse2027-nier
python scripts/check_anonymous_submission_package.py --track icse2027-nier --build --run-smoke
```

Output:

- `dist/anonymous/icse2027-nier-anonymous-artifact.zip`

The script copies only the harness, benchmark cases, selected recorded rows,
regenerated result tables, fixture evidence, tests, and anonymous NIER source. It refuses to
package author-identifying strings such as public profile, repository, Zenodo,
or active arXiv endorsement references.

The independent checker verifies required files, forbidden path classes, unsafe
zip paths, author-identifying strings, and the reviewer smoke path.

Reviewer no-dependency check inside the extracted package:

```powershell
python scripts/run_demo_walkthrough.py
python scripts/smoke_test.py
```
