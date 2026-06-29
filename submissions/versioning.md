# Versioning And Artifact Policy

## Branches

Use one durable branch per submission target:

- `main`: public preprint, Zenodo artifact baseline, reproducible pilot results.
- `submission/icse2027-nier`: anonymized NIER paper and anonymous artifact
  package notes.
- `submission/saner2027-tool-demo`: 5-page IEEE tool demo paper and SANER
  screencast details.
- `submission/saner2027-short-paper`: anonymized SANER short paper and
  anonymous artifact package notes.

Do not mix double-anonymous materials with the public GitHub/Zenodo URLs in the
same final PDF.

## Tags And Releases

Tag only versions that leave the repository:

- `v0.1.0-preprint`: current public preprint and Zenodo version.
- `v0.3.0-icse2027-nier-submission`: exact anonymized NIER submission package.
- `v0.4.0-saner2027-tool-demo-submission`: exact SANER demo submission package.
- `v0.5.0-saner2027-short-paper-submission`: exact SANER short-paper package.
- `v1.0.0-camera-ready`: accepted camera-ready package, if any.

Each release should include:

- PDF.
- Source archive.
- Artifact archive or link.
- SHA-256 hashes for PDF and artifact archive.
- Reproduction command list.
- Video URL, only for non-anonymous tracks or camera-ready versions.

## Anonymity Boundary

Public tracks can mention:

- Song Luo.
- https://github.com/rrrrrredy/agent-harness-paper
- https://doi.org/10.5281/zenodo.20907471
- YouTube demo URL.

Double-anonymous tracks must remove or replace:

- author names and email addresses;
- personal GitHub, Zenodo, arXiv, Google, YouTube, or profile links;
- first-person references to prior work;
- repository names that identify the author;
- acknowledgments and operational process traces.

For double-anonymous review, prefer an EasyChair additional-material zip. If a
link is unavoidable, use an anonymized artifact service and warn if it may reveal
identity, following the target track instructions.
