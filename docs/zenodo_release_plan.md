# Zenodo Release Plan

## Published Record

- Archive mode: public Zenodo record.
- Access right: open.
- License: CC BY 4.0 for the archived artifact package.
- Working repository: public at https://github.com/rrrrrredy/agent-harness-paper.
- Published record: https://zenodo.org/records/20907471
- Version DOI: https://doi.org/10.5281/zenodo.20907471
- All-versions DOI: https://doi.org/10.5281/zenodo.20907470
- Uploaded files: checked PDF plus `dist/agent-harness-paper-artifact.zip`.

## Official Basis

- Zenodo's new-upload help describes uploading files, adding metadata, setting restrictions, saving, and publishing: https://help.zenodo.org/docs/deposit/create-new-upload/
- Zenodo's license help states that the license field is required and that Zenodo defaults to Creative Commons Attribution 4.0 International: https://help.zenodo.org/docs/deposit/describe-records/licenses/
- Zenodo's GitHub metadata help documents `.zenodo.json` for release archiving: https://help.zenodo.org/docs/github/describe-software/zenodo-json/

## Metadata

- Title: Thin Harness, Strong Contracts: Production-Oriented Agent Harnesses for Stateful AI Agents
- Creator: Luo, Song
- Upload type: publication
- Publication type: preprint
- Language: English
- License: `cc-by-4.0`
- Version: `0.1.0-preprint`

## Release Steps

1. Completed: ran validation before release.
2. Completed: built `dist/agent-harness-paper-artifact.zip` with `python scripts/build_artifact_archive.py`.
3. Completed: downloaded the checked PDF artifact from GitHub Actions.
4. Completed: uploaded the PDF and zip to Zenodo as a new public record.
5. Completed: confirmed metadata matches `.zenodo.json`.
6. Completed: published the Zenodo record.
7. Completed: recorded the DOI in `paper/metadata.json`, `artifact_manifest.json`, `docs/artifact_release_index.md`, and `CHANGELOG.md`.
