# VANTAGE Technology Radar — Workbook Analysis

Source: `data/VANTAGE-Technology-Radar.xlsx`

Read-only scan. No cell in the workbook was modified. Findings are flagged, not corrected — fixes are a human judgment call.

## Per-sheet row counts and cell anomalies

### Knowledgebase

- Total data rows: 33
- Empty rows: 0 (rows none)
- Populated rows: 33
- Anomalous cells: 0

### Deprecated

- Total data rows: 2
- Empty rows: 0 (rows none)
- Populated rows: 2
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

- Vocabulary size: 28; distinct values in use: 14
- Used but **not in `Vocabulary`**: none
- In `Vocabulary` but **never used**: `Data Protection`, `Data architecture, analysis and design`, `Data curation and archival`, `Data identity and mapping`, `Data integration and warehousing`, `Data quality management`, `Data rescue`, `Evaluation`, `Explainable and Interpretable`, `FAIR data`, `Fair (harmful bias managed)`, `Model selection`, `Privacy-Enhanced`, `Safe`

### ALAF Checklist Mapping (`controlled_multi`)

- Vocabulary size: 7; distinct values in use: 6
- Used but **not in `Vocabulary`**: none
- In `Vocabulary` but **never used**: `Deidentify Data`

### Maturity Level (`controlled_single`)

- Vocabulary size: 4; distinct values in use: 4
- Used but **not in `Vocabulary`**: none
- In `Vocabulary` but **never used**: none

## Missing controlled values

Populated rows with an empty controlled-vocabulary cell.

**Knowledgebase**
- row 2: `022e4e1c` is missing `ALAF Checklist Mapping`
- row 3: `2e9b6b2d` is missing `ALAF Checklist Mapping`
- row 4: `161f1860` is missing `ALAF Checklist Mapping`
- row 5: `abbd844c` is missing `ALAF Checklist Mapping`
- row 6: `b71baded` is missing `ALAF Checklist Mapping`
- row 7: `2b23adbb` is missing `ALAF Checklist Mapping`
- row 8: `d6d28dfa` is missing `ALAF Checklist Mapping`
- row 9: `f488464f` is missing `ALAF Checklist Mapping`
- row 10: `dbe3741e` is missing `ALAF Checklist Mapping`
- row 11: `ddd42289` is missing `ALAF Checklist Mapping`
- row 12: `c7e95f61` is missing `ALAF Checklist Mapping`
- row 13: `73426de0` is missing `ALAF Checklist Mapping`
- row 14: `3294a13f` is missing `ALAF Checklist Mapping`
- row 15: `f51ea180` is missing `ALAF Checklist Mapping`
- row 16: `89f36cc1` is missing `ALAF Checklist Mapping`
- row 17: `4ccfda21` is missing `ALAF Checklist Mapping`
- row 18: `2e24be4d` is missing `ALAF Checklist Mapping`
- row 21: `3758624e` is missing `ALAF Checklist Mapping`
- row 22: `8a50b5eb` is missing `ALAF Checklist Mapping`
- row 23: `763797cd` is missing `ALAF Checklist Mapping`
- row 24: `2d2470f7` is missing `ALAF Checklist Mapping`
- row 28: `0d0a50a7` is missing `ALAF Checklist Mapping`
- row 30: `5f3954c2` is missing `ALAF Checklist Mapping`
- row 32: `b39dc1d1` is missing `ALAF Checklist Mapping`

**Deprecated**
- row 2: `805047b4` is missing `ALAF Checklist Mapping`
- row 3: `bfda8877` is missing `ALAF Checklist Mapping`

**SOTA Coding Agents Benchmarks**
- row 2: `ba114fad` is missing `ALAF Checklist Mapping`
- row 3: `4c170f7e` is missing `ALAF Checklist Mapping`
- row 4: `b9ed03e7` is missing `ALAF Checklist Mapping`
- row 5: `f487cdc5` is missing `ALAF Checklist Mapping`
- row 6: `f37d4051` is missing `ALAF Checklist Mapping`
- row 7: `acbc7354` is missing `ALAF Checklist Mapping`
- row 8: `edd19b89` is missing `ALAF Checklist Mapping`

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

### ALAF Checklist Mapping

- Standards-backed terms (0): none
- **Not backed by any standard** (7): `Agent Manifesto`, `Deidentify Data`, `Human Approval Gate`, `Provenance and Reversibility`, `Remediate Oversharing`, `Runtime PII Screening`, `Zero Data Retention`

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

## ALAF Checklist Mapping vs the checklist

Source: `ALAF_CHECKLIST.md` (7 items, 7 vocabulary terms)

In sync: every checklist item has a term and every term has an item.

Matched as deliberate short forms:

- `Deidentify Data` -> Deidentify Data Before Agent Access
- `Runtime PII Screening` -> Runtime PII Screening as an Agent Tool
