# Security Policy

## Reporting a Vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities.

Instead, use GitHub's private vulnerability reporting for this repository:

1. Go to the [Security tab](https://github.com/MEDGALIA/ALAF/security).
2. Click **"Report a vulnerability"**.
3. Describe the issue, including steps to reproduce, potential impact, and
   any suggested fix if you have one.

This opens a private advisory visible only to the maintainers — no public
disclosure, no email required. We'll acknowledge reports as promptly as we
can and keep you updated as we investigate and address the issue.

## Scope

This repository contains data-processing tooling (`src/scripts/`), a
GitHub Action (`.github/workflows/`), and a curated knowledge base
(`data/`). Relevant concerns include (but aren't limited to):

- Vulnerabilities in the sync scripts (e.g. unsafe deserialization, path
  traversal when reading/writing the xlsx or JSON files)
- Issues in the GitHub Actions workflow that could allow unauthorized
  writes, secret exposure, or supply-chain compromise
- Dependency vulnerabilities in `src/scripts/requirements.txt`

Data-quality issues in the knowledge base itself (e.g. an incorrect or
outdated entry) are not security reports — please file those as a regular
[GitHub issue](https://github.com/MEDGALIA/ALAF/issues) instead.

## Supported Versions

ALAF is pre-release / early development (see [README](README.md#status)).
There are no tagged releases yet, so security fixes are applied to `main`.
