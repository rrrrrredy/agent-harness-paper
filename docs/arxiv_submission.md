# arXiv Submission Notes

## Current Decision

- Route: public arXiv-style preprint.
- Template: standard LaTeX `article` class, kept arXiv-friendly.
- Author metadata: non-anonymous, Song Luo.
- Suggested primary category: `cs.SE` because the paper is about agent harness infrastructure, testing, debugging, tool interfaces, and programming-environment behavior.
- Suggested cross-list: `cs.AI` because the work concerns AI agents and tool use.
- Artifact pointer: https://doi.org/10.5281/zenodo.20907471; the public GitHub repository is available at https://github.com/rrrrrredy/agent-harness-paper.

## Official Basis

- arXiv category taxonomy says `cs.SE` covers software engineering, including design tools, software metrics, testing/debugging, and programming environments: https://arxiv.org/category_taxonomy
- arXiv endorsement help says an endorsement request uses a six-character alphanumeric endorsement code: https://info.arxiv.org/help/endorsement.html

## Submission Checklist

1. Build or download the checked PDF from the GitHub Actions artifact.
2. Build `dist/agent-harness-paper-artifact.zip` and upload it to Zenodo.
3. Use the Zenodo artifact DOI `10.5281/zenodo.20907471` in the arXiv submission comments if appropriate.
4. If arXiv requests endorsement, use the formal arXiv request email and `docs/arxiv_endorsement_email.md` as the email draft; do not commit active endorsement links or codes to public artifacts.
5. Submit as non-anonymous author Song Luo.

## Pending External Inputs

- arXiv endorsement response, if arXiv requires external endorsement before submission.
