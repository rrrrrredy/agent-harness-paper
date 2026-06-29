# Adversarial Review Summary

Date: 2026-06-29.

Three independent review passes were run for the submission variants. The
shared conclusion is that the public preprint is useful as a source artifact but
is not directly submit-ready for any of the target tracks.

## ICSE Tool Demonstration And Data Showcase

Readiness: fail today, 35/100.

Best route: Tool Demonstration, not primarily Data Showcase.

Main blockers:

- current preprint is not IEEE four-page demo format;
- video URL and 3-5 minute YouTube demo are missing;
- reviewer path must be no-credential and easy to run;
- paper must sell a concrete replayable harness tool, not a broad framework;
- tool distribution must be easier than asking reviewers to build a research
  repo from scratch.

Required changes:

- convert to `IEEEtran` 10pt conference format;
- reduce to four pages including references;
- add public tool URL, usage instructions, and video URL at the end of the
  abstract;
- show one runnable scenario: case definition, local run, state diff,
  permission failure, regenerated table;
- keep provider results bounded and non-leaderboard.

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
drafts for all four routes, generated public backup demo videos, and rewrote
the ICSE NIER and SANER Short Paper versions into anonymous short-paper
arguments. The main remaining blockers are:

- ICSE Tool Demonstration still needs the official YouTube URL inserted before
  submission, even though a GitHub Release backup video is public.
- ICSE NIER still needs a true anonymous supplemental package rather than
  pointing reviewers at the public author repository.
- SANER Short Paper still needs stronger repository-fixture evidence before it
  should be treated as a competitive empirical short paper.
- No local IEEE PDF compile check has been run because this machine currently
  lacks `latexmk`, `pdflatex`, and `tectonic`.
