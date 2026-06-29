# ICSE 2027 Tool Demonstration And Data Showcase

## Position

Submit as a tool demonstration with a data-showcase component.

Core artifact: a replayable pilot harness for stateful agent contracts. The
tool defines benchmark cases, mock state, tool permissions, prompt variants,
runner logs, state-diff metrics, uncertainty tables, and regeneration scripts.

The paper should not claim to be a broad model benchmark. It should claim that
the artifact demonstrates how to evaluate production-oriented agent harness
contracts in a small but inspectable setting.

## Official Constraints

- Format: IEEE conference format.
- Length: four pages maximum, inclusive of references, figures, tables, and
  appendices.
- Review: single-anonymous; include author identity.
- Artifact: link to a publicly available tool and usage instructions; open
  source repository link is appropriate.
- Distribution expectation: reviewers should not need to build a complex system
  from scratch. The demo path must work from a normal Python checkout and from
  the archived artifact without provider credentials.
- Video: 3-5 minutes, online at submission time, uploaded to YouTube and
  accessible during review.
- Submission site: https://icse27demos.hotcrp.com/
- Submission deadline: Friday 23 October 2026, AoE.

Official page: https://conf.researchr.org/track/icse-2027/icse-2027-demonstrations

## Paper Conversion

Use `paper/main.tex` as the source of claims, but rewrite as a tool paper:

1. Problem: final-answer evaluation misses stateful agent failures.
2. Artifact: replayable harness with cases, mock tools, policies, and metrics.
3. Demo scenario: run validation, inspect one permission failure, regenerate
   tables, compare prompt variants.
4. Usefulness: lets researchers and practitioners add state-diff and permission
   contracts around agent workflows.
5. Evidence: 24 cases, deterministic reference runner, two live provider runs,
   no leaderboard framing.
6. Availability: GitHub, Zenodo DOI, release tag, YouTube demo.

Temporary backup video URL before YouTube upload:
https://github.com/rrrrrredy/agent-harness-paper/releases/download/v0.1.0-preprint/agent-harness-icse-tool-demo-video.mp4

## Blocking Risks

- The current repository is useful but not packaged as an easy-to-run tool for
  reviewers who will not build from scratch.
- The video is generated and published as a GitHub Release backup asset, but
  ICSE still requires a YouTube URL before submission.
- The four-page limit forces aggressive compression.
- The term "harness" must be operationalized through commands and output, not
  only described as a concept.
- The abstract must append the video URL before submission.

## Concrete Submission Steps

1. Create or update branch `submission/icse2027-tool-demo`.
2. Finalize `submissions/icse2027-tool-demo/paper/main.tex`.
3. Generate PDF in IEEE conference format.
4. Run `python scripts/run_checks.py --mode validate`.
5. Run `python scripts/run_demo_walkthrough.py`.
6. Run `python scripts/make_demo_video.py --track icse-tool-demo`.
7. Upload `dist/videos/icse-tool-demo/agent-harness-demo.mp4` to YouTube as
   Unlisted unless the final decision is Public.
8. Insert the YouTube URL at the end of the paper abstract and in HotCRP.
9. Create tag `v0.2.0-icse2027-tool-demo-submission`.
10. Create a GitHub release with PDF, source zip, artifact zip hashes, and video
   URL.
11. Submit PDF at https://icse27demos.hotcrp.com/.
