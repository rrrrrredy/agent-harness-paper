# Conference Submission Workspace

This directory keeps conference-specific versions separate from the public
preprint in `paper/`. The repository strategy is:

- `main` remains the public, reproducible preprint and artifact baseline.
- `codex/submission-prep` prepares conference-specific drafts, checklists, and
  the remaining conference-specific artifacts.
- Future submission branches should be named by track, for example
  `submission/icse2027-nier`, `submission/saner2027-tool-demo`, and
  `submission/saner2027-short-paper`.
- Release tags should mark only externally shared versions, for example
  `v0.3.0-icse2027-nier-submission` and `v1.0.0-camera-ready`.

## First-Principles Split

The work has two remaining submission shapes.

1. Public artifact track: SANER Tool Demo. This track can use the public GitHub
   repository, Zenodo DOI, author name, and the GitHub Release screencast. The
   paper should sell a usable tool artifact, not a broad research claim.
2. Double-anonymous idea or short-paper tracks: ICSE NIER and SANER Short
   Papers and Posters. These tracks need anonymized paper text and either an
   anonymous artifact package or a statement that the public repository will be
   disclosed after review.

The same core artifact supports both, but the evidence emphasis changes:

- Tool demo: installation, runnable harness, results regeneration, short video,
  reviewer path, DOI, and concrete use cases.
- NIER: thesis, research agenda, design principle, and bounded pilot evidence.
- SANER short paper: software evolution framing around repo state, diffs,
  test oracles, replay, maintenance risk, and agent-induced side effects.

## Current Tracks

| Track | Review model | Page target | Artifact mode | Primary status |
|---|---:|---:|---|---|
| ICSE 2027 NIER | Double-anonymous | 4 pages main text plus 1 references-only page | Anonymous package or deferred public link | Good idea-paper target after anonymization |
| SANER 2027 Tool Demo | Single-anonymous | 5 pages, references included | Public GitHub, optional YouTube/screencast | Strong fallback or parallel target |
| SANER 2027 Short Papers and Posters | Double-anonymous | 6 pages, references included | Anonymous package preferred | Needs stronger SE-analysis framing |

## Official Sources To Recheck Before Submission

- ICSE 2027 NIER:
  https://conf.researchr.org/track/icse-2027/icse-2027-new-ideas-and-emerging-results--nier-
- SANER 2027 Tool Demo:
  https://conf.researchr.org/track/saner-2027/saner-2027-tool-demo-track
- SANER 2027 Short Papers and Posters:
  https://conf.researchr.org/track/saner-2027/saner-2027-short-papers-and-posters-track
