# VANTAGE Technology Radar — Workbook Analysis

Source: `data/VANTAGE-Technology-Radar.xlsx`

Read-only scan. No cell in the workbook was modified. Findings are flagged, not corrected — fixes are a human judgment call.

## Per-sheet row counts and cell anomalies

### Knowledgebase

- Total data rows: 42
- Empty rows: 10 (rows 34–43)
- Populated rows: 32
- Anomalous cells: 0

### Deprecated

- Total data rows: 1
- Empty rows: 0 (rows none)
- Populated rows: 1
- Anomalous cells: 0

### SOTA Coding Agents Benchmarks

- Total data rows: 7
- Empty rows: 0 (rows none)
- Populated rows: 7
- Anomalous cells: 0

## Column coverage

- Columns in data tabs but **not documented** in `Dictionary`: none
- Documented in `Dictionary` but **present in no data tab**: none

## Vocabulary coverage

Only columns whose `Value Type` is a controlled vocabulary are checked; free-text columns are skipped by design.

### Resource Type (`controlled_single`)

- Vocabulary size: 14; distinct values in use: 14
- Used but **not in `Vocabulary`**: none
- In `Vocabulary` but **never used**: none

### Agentic Features Covered (`controlled_multi`)

- Vocabulary size: 30; distinct values in use: 29
- Used but **not in `Vocabulary`**: none
- In `Vocabulary` but **never used**: `Context window management`

### Topic Focus (`controlled_multi`)

- Vocabulary size: 28; distinct values in use: 11
- Used but **not in `Vocabulary`**: none
- In `Vocabulary` but **never used**: `Accountable and Transparent`, `Data Protection`, `Data architecture, analysis and design`, `Data curation and archival`, `Data identity and mapping`, `Data integration and warehousing`, `Data quality management`, `Data rescue`, `Evaluation`, `Explainable and Interpretable`, `FAIR data`, `Fair (harmful bias managed)`, `Model selection`, `Privacy-Enhanced`, `Safe`, `Secure and Resilient`, `Valid and Reliable`

### Maturity Level (`controlled_single`)

- Vocabulary size: 4; distinct values in use: 4
- Used but **not in `Vocabulary`**: none
- In `Vocabulary` but **never used**: none

## Missing controlled values

None — every populated row has a value in each controlled column that applies to it.

## Ontology coverage

Declared standards: `EDAM` (http://edamontology.org/topic_3071), `NIST-AI-RMF` (https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf), `ACM-CCS` (https://dl.acm.org/ccs), `Schema.org` (https://schema.org/CreativeWork)

### Resource Type

- Standards-backed terms (10): `API Reference → Schema.org`, `Benchmark Collection → Schema.org`, `Documentation → Schema.org`, `Github Code Repository → Schema.org`, `Governance Guidance → Schema.org`, `Reference Architecture → Schema.org`, `Scientific Literature → Schema.org`, `Security Guidance & Resources → Schema.org`, `Specification → Schema.org`, `Whitepaper → Schema.org`
- **Not backed by any standard** (4): `Container Registry`, `Enterprise Control Interface`, `Inference Framework`, `Local Application Sandbox`

### Agentic Features Covered

- Standards-backed terms (5): `Cybersecurity → ACM-CCS`, `Evaluation / testing → ACM-CCS`, `FAIR data → EDAM`, `Retrieval Agents → ACM-CCS`, `Retrieval → ACM-CCS`
- **Not backed by any standard** (25): `API Integration`, `Agent Patterns`, `Agent frameworks`, `Coding Agents`, `Context window management`, `Deployment patterns`, `Governance`, `Hooks`, `MCP`, `Model Integration`, `Multi-Agent Patterns`, `Notebook Agents`, `Orchestration`, `Risk Controls`, `Safe Tool Use`, `Safety / guardrails`, `Sandbox`, `Server Integration`, `Server Patterns`, `Skills`, `Tool-Ready Endpoints`, `Tools`, `Triggers`, `Workflow Agents`, `Workflow Automation`

### Topic Focus

- Standards-backed terms (22): `Accountable and Transparent → NIST-AI-RMF`, `Architecture → ACM-CCS`, `Data Protection → EDAM`, `Data architecture, analysis and design → EDAM`, `Data curation and archival → EDAM`, `Data governance → EDAM`, `Data identity and mapping → EDAM`, `Data integration and warehousing → EDAM`, `Data quality management → EDAM`, `Data rescue → EDAM`, `Deployment → NIST-AI-RMF`, `Evaluation → ACM-CCS`, `Explainable and Interpretable → NIST-AI-RMF`, `FAIR data → EDAM`, `Fair (harmful bias managed) → NIST-AI-RMF`, `Implementation → ACM-CCS`, `Privacy-Enhanced → NIST-AI-RMF`, `Safe → NIST-AI-RMF`, `Secure and Resilient → NIST-AI-RMF`, `Security → ACM-CCS`, `Valid and Reliable → NIST-AI-RMF`, `Workflows → EDAM`
- **Not backed by any standard** (6): `Compute Infrastructure`, `Governance`, `Infrastructure Security`, `Model selection`, `Network Isolation`, `Self‑hosted AI`

### Maturity Level

- Standards-backed terms (0): none
- **Not backed by any standard** (4): `Deprecated`, `Emerging`, `Mature`, `Research`

## Review candidates (near-duplicates, deliberately not auto-merged)

Term pairs where one term's words are a subset of the other's. These were left alone because merging them is a semantic judgment, not a spelling fix.

**Agentic Features Covered**
- `Tools` vs `Safe Tool Use`
- `Retrieval` vs `Retrieval Agents`

**Topic Focus**
- `Architecture` vs `Data architecture, analysis and design`
- `Security` vs `Infrastructure Security`
- `Governance` vs `Data governance`
