# Adversarial Review Summary

Date: 2026-06-29.

Adversarial review now covers the remaining submission routes.

## ICSE NIER

Readiness: fail today, 28/100.

Best route: new-idea paper around the distinction between capability-patch
harnesses and system-boundary harnesses.

Main blockers:

- NIER is four pages of main text plus one references-only page, not an
  eight-page target;
- double-anonymous review is currently violated by names, GitHub, Zenodo,
  metadata, and first-party evidence phrasing;
- required `Future Plans` section must be present;
- related work and novelty defense are too thin;
- pilot evidence must be framed as feasibility evidence, not a regular
  empirical result.

Required changes:

- anonymize the paper and artifact;
- compress to problem, new idea, contract taxonomy, one pilot table, and
  `Future Plans`;
- remove public author links and personal project identifiers;
- strengthen related work against agent benchmarks, tool-use security,
  agent-computer interfaces, replay/provenance, and SE evaluation methods.

## SANER Tool Demo / Short Paper

Tool Demo readiness: fail today but salvageable, 42/100.

Short Paper readiness: fail today, 28/100.

Best route: SANER Tool Demo after reframing around repository-changing agents
and maintenance risk. Short Paper needs an anonymized, narrower empirical or
tool-oriented story.

Main blockers:

- current framing is too general for SANER;
- repository-state and patch-level oracles are shallow;
- replay is currently approximated by the existence of actions;
- double-anonymous short-paper version is not ready;
- actual fixture repositories, git diffs, tests, and replay logs would
  strengthen the SANER case.

Required changes:

- frame the tool as a repository-state harness for coding and maintenance
  agents;
- emphasize diffs, tests, validation commands, permission gates, and replay;
- keep live providers optional and use recorded traces for reviewers;
- for Short Paper, create an anonymous package and cut broad production claims.

## Post-Hardening Note

After the first adversarial pass, the submission branch added targeted LaTeX
drafts for the remaining routes, generated a public SANER backup screencast,
rewrote the ICSE NIER and SANER Short Paper versions into anonymous short-paper
arguments, added an anonymous NIER supplemental artifact builder, and added a
concrete SANER repository fixture.

The main remaining blockers are:

- ICSE NIER needs a final anonymous packaging pass immediately before
  submission.
- SANER Short Paper has one concrete repository fixture, but not a large
  empirical study; keep claims narrow.
- Local IEEE PDF tooling is absent, but GitHub Actions PDF workflow run
  `28347502768` successfully built the targeted PDFs.

## Final Sub-Agent Adversarial Pass

Three independent sub-agent reviews were run for SANER Tool Demo, ICSE NIER,
and SANER Short Paper.

Resolved findings:

- Anonymous packages no longer include public-release tests or public artifact
  traces. The builder now creates track-specific anonymous trees, sanitizes the
  project slug in packaged metadata and raw rows, omits repository fixtures from
  the ICSE NIER package, and keeps repository fixtures only in the SANER Short
  package.
- The anonymous package checker now validates each track against its actual
  file set and a broader deanonymization denylist.
- The anonymous package README no longer advertises `pytest`; the supported
  reviewer path remains the no-dependency walkthrough and smoke commands.
- ICSE NIER and SANER Short no longer include the Deli AutoResearch citation in
  the double-anonymous bibliography.
- The SANER Short paper now reports a compact 24-case pilot snapshot and keeps
  the results descriptive rather than benchmark-like.
- The repository fixture runner now rejects absolute paths and `..` path
  escapes.
- SANER Tool Demo paper/package links now target the exact planned submission
  tag instead of the repository default branch.
- SANER Tool Demo reviewer commands no longer start with a package builder that
  depends on ignored local PDF artifacts.
- The SANER package manifest now hashes the runnable harness surface, benchmark
  cases, raw rows, validation scripts, fixture inputs, fixture outputs, tests,
  and supporting evidence.
- Public release docs now reflect that the GitHub repository is public.

Residual risks:

- The SANER screencast is still mostly a narrated walkthrough asset rather than
  a live terminal recording. It is acceptable as a backup video, but a live
  screencast would be stronger if video production time is available.
- The exact SANER submission tag must be created after the final commit so the
  paper URL resolves to the intended snapshot.
- ICSE NIER and SANER Short should be rebuilt by CI after the final text edits
  before any upload.
