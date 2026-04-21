# Geothermal Drilling Cost

A collaborative, open repository for analyzing **what drives geothermal drilling costs** and how drilling outcomes affect project bankability.

## Why this project exists
Geothermal projects are often constrained by upfront drilling risk. This repo is designed to help contributors build transparent, reusable analysis around:
- well cost and depth drivers,
- dry-well risk and success-rate uncertainty,
- schedule and inflation sensitivity,
- implications for project finance and de-risking tools.

## Project goals
1. Build a clean, documented dataset for geothermal drilling economics.
2. Create scenario models for technical and financial uncertainty.
3. Produce clear visual outputs that can support developers, investors, and policymakers.
4. Keep the work reproducible and easy for new contributors to extend.

## Repository structure
```text
.
├── .github/
│   ├── ISSUE_TEMPLATE/
│   └── pull_request_template.md
├── data/
│   ├── raw/
│   └── processed/
├── docs/
├── models/
│   ├── drilling-risk/
│   └── project-economics/
├── notebooks/
├── results/
│   ├── charts/
│   └── tables/
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── LICENSE
├── PROJECT_AUDIT.md
├── README.md
└── SECURITY.md
```

## Getting started
1. Fork the repository.
2. Read [CONTRIBUTING.md](CONTRIBUTING.md).
3. Pick an issue (or open one).
4. Submit a pull request using the PR template.

## Contribution areas
- Data collection and source validation
- Cost-model development
- Notebook cleanup and reproducibility
- Visualizations and summary tables
- Documentation and methodology reviews

## Suggested next content
- `docs/methodology.md`
- `docs/kenya-market-context.md`
- Baseline drilling risk model in `models/drilling-risk/`
- Scenario outputs in `results/charts/` and `results/tables/`

## Governance
Please review before contributing:
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)

## License
This project is licensed under the MIT License. See [LICENSE](LICENSE).
