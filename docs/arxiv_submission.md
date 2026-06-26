# arXiv Submission Notes

## Current Decision

- Route: public arXiv-style preprint.
- Template: standard LaTeX `article` class, kept arXiv-friendly.
- Author metadata: non-anonymous, Song Luo.
- Suggested primary category: `cs.SE` because the paper is about agent harness infrastructure, testing, debugging, tool interfaces, and programming-environment behavior.
- Suggested cross-list: `cs.AI` because the work concerns AI agents and tool use.
- Artifact pointer: Zenodo DOI after upload; do not expose the private GitHub working repository as the public artifact link.

## Official Basis

- arXiv category taxonomy says `cs.SE` covers software engineering, including design tools, software metrics, testing/debugging, and programming environments: https://arxiv.org/category_taxonomy
- arXiv endorsement help says an endorsement request uses a six-character alphanumeric endorsement code: https://info.arxiv.org/help/endorsement.html

## Submission Checklist

1. Build or download the checked PDF from the GitHub Actions artifact.
2. Build `dist/agent-harness-paper-artifact.zip` and upload it to Zenodo.
3. Add the Zenodo DOI to `paper/metadata.json`, `docs/artifact_release_index.md`, and the arXiv submission comments if appropriate.
4. If arXiv requests endorsement, obtain the six-character endorsement code from the arXiv submission flow and use `docs/arxiv_endorsement_email.md` as the email draft.
5. Submit as non-anonymous author Song Luo.

## Pending External Inputs

- arXiv endorsement code, only if arXiv asks for one.
- Zenodo DOI, after publication.
