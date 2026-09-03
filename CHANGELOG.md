# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
once a first release is tagged. Until then, changes are tracked under
`[Unreleased]`.

## [Unreleased]

### Added

- VT Radar knowledge base: `data/VANTAGE-Technology-Radar.xlsx` with
  `Knowledgebase`, `Deprecated`, and `SOTA Coding Agents Benchmarks` data
  tabs, plus normalized `Dictionary` / `Vocabulary` / `Standards` metadata
  tabs driving a schema-based xlsx ⇄ JSON sync.
- `src/scripts/xlsx_to_json.py` — converts the workbook into `data/json/`,
  with content-hash-based verification tracking (`Verified By` / `Last
  Verified` cleared automatically when a row's content changes since the
  last known baseline).
- `src/scripts/tech_radar_analysis.py` — read-only workbook analysis
  (row/column coverage, controlled-vocabulary coverage, ontology-mapping
  coverage, near-duplicate review candidates), written to
  `data/reports/workbook_analysis.md`.
- `src/scripts/radar_sync_common.py` — shared schema-loading helpers for the
  VT Radar tooling.
- `src/scripts/docx_to_md.py` and `src/scripts/md_to_html.py` — document
  conversion pipeline for `developer_guides/`.
- Controlled-vocabulary terms backed by external standards where a genuine
  match exists: EDAM, NIST AI RMF 1.0, ACM Computing Classification System
  2012, and Schema.org.
- GitOps infrastructure: `.github/workflows/xlsx-to-json.yml` and
  `.github/CODEOWNERS` requiring curator review of `data/json/**` changes.
- Developer documentation in `developer_guides/`, rendered to static HTML in
  `developer_guides_html/`.
- `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, and this changelog.

[Unreleased]: https://github.com/MEDGALIA/ALAF/commits/main
