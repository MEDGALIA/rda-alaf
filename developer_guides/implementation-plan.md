# Implementation Plan

The implementation plan has two steps so far :

1. VT Radar xlsx ⇄ JSON Two-Way Sync (Status: Started)
2. Agentic Process to update the VT Radar (Not implemented)

## VT Radar xlsx ⇄ JSON Two-Way Sync

### Context

`data/VANTAGE-Technology-Radar.xlsx` is the human-facing "Tech Radar" — a workbook a person downloads, reads, and edits in Excel. 4 tabs: `Knowledgebase`, `Dictionary`, `Deprecated`, `SOTA Coding Agents Benchmarks`. `Knowledgebase`, `Deprecated`, and `SOTA Coding Agents Benchmarks` share a `Last Verified` + `Verified By` column pair; `Dictionary` is a plain glossary with no verification columns.

We want a machine-readable mirror in `data/json/` (one JSON file per tab) that agents can read and edit directly, plus a way to publish those edits back into the xlsx for the human to see. Any add/remove/edit of a json row must clear that row's `Verified By`/`Last Verified` — a human re-approving content they never saw would be a false claim. Old values aren't lost; they're recoverable from git history on the json files.

The workbook has some pre-existing messy data (mostly empty formatted rows, a few type-mismatched cells) — see `drafts/workbook_errors.md`. That's reported only, never auto-corrected.

### GitOps Implementation

**Decision**: git/GitHub pull requests are the versioning, review, and audit system for `data/json/*.json` — chosen over a custom status-field model or an event-sourced log, since GitHub's own review/merge/history mechanics already cover this at the project's current scale.

**Roles**
- **Curator** — required PR reviewer for `data/json/**` (`.github/CODEOWNERS` + branch protection). Approving a PR is the act of verifying.
- **Publisher** — merges the PR and triggers the xlsx rebuild. Can be the same person as curator.

**Source of truth**: `data/json/*.json`, fully git-tracked. Git history (`git log`/`git blame`) is the audit trail — no separate backup files or log. The xlsx is a build artifact: regenerated from json and attached to a GitHub Release, not committed as a binary diff on every publish.

**Workflow**
1. Bootstrap (one time): `xlsx_to_json.py` converts the xlsx into `data/json/*.json`.
2. Ongoing edits go through a PR — either directly to the json, or by uploading a changed xlsx (a GitHub Action converts the upload into the same kind of json diff).
3. Any added/removed/edited row has `Verified By`/`Last Verified` cleared automatically as part of that conversion.
4. Curator reviews and approves the PR.
5. Publisher merges, then triggers `json_to_xlsx.py` to regenerate the xlsx and publish it as a new Release.

No git CLI or branch-pushing is required of curators or publishers — every step is available through GitHub's native web UI (edit-in-browser, drag-and-drop upload, "Approve" button, "Merge" button).

**Status**

| Component | Status |
| --- | --- |
| `src/scripts/radar_sync_common.py` | Done |
| `src/scripts/tech_radar_quality_report.py` | Done — see `drafts/workbook_errors.md` |
| `.github/CODEOWNERS` for `data/json/**` | Done — names `@pbuendia` |
| Branch protection on `main` | Done — PR + 1 code-owner approval required; admin bypass allowed (no second curator yet, flip off once one exists); no required status checks yet (no CI) |
| `src/scripts/xlsx_to_json.py` | Not started |
| GitHub Action — xlsx upload → json diff | Not started |
| `src/scripts/json_to_xlsx.py` | Not started |
| GitHub Action — publish (`workflow_dispatch` → Release) | Not started |
| Developer/user documentation | In progress (this file) |

**Deferred**: a GitHub Pages UI as a friendlier front-end for the same GitHub API actions (edit, upload, approve, merge, publish) — not required to start; would use a fine-grained personal access token for auth initially.

## Agentic Process to update the VT Radar

Not implemented. No design decisions made yet.
