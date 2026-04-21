# Contributing Guide

Thanks for your interest in contributing to this repository.

## Ways to contribute
- Add data sources and document provenance.
- Improve modeling assumptions and sensitivity design.
- Add or refactor notebooks for reproducibility.
- Improve documentation and interpretation of results.

## Development workflow
1. Fork the repository and create a feature branch.
2. Make focused commits with descriptive messages.
3. Keep notebooks and docs clear, structured, and reproducible.
4. Open a pull request using the PR template.

## Branch and commit naming (recommended)
- Branches: `feat/<short-topic>`, `fix/<short-topic>`, `docs/<short-topic>`
- Commit style: imperative (e.g., `Add drilling cost assumptions table`)

## Pull request checklist
- [ ] Changes are scoped and explained clearly.
- [ ] Documentation updated where needed.
- [ ] New assumptions include source notes.
- [ ] Output artifacts (charts/tables) are added where relevant.

## Data and sourcing expectations
- Cite data sources in notebook markdown or docs.
- Keep raw data in `data/raw/` and cleaned data in `data/processed/`.
- Avoid committing confidential or licensed-restricted data.

## Community expectations
By participating, you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).
