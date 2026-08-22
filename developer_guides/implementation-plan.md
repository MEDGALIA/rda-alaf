# Implementation Plan

The implementation plan has two steps so far:

1. VT Radar xlsx ⇄ JSON Two-Way Sync (Status: In progress)
2. Agentic Process to update the VT Radar (Not implemented)
3. Agentic Assessment Landscape Framework (ALAF)

## VT Radar xlsx ⇄ JSON Two-Way Sync

### Context

`data/VANTAGE-Technology-Radar.xlsx` is the human-facing "Tech Radar" — a workbook a person downloads, reads, and edits in Excel. It has three **data** tabs which share `ID`, `Last Verified`, `Verified By`, and `Added/Edited By` columns, and three **metadata** tabs that define the schema rather than holding records.

**Data Tabs:**

| Tab | Purpose |
| --- | --- |
| `Knowledgebase` | Active tracked resources |
| `Deprecated` | Resources no longer valid or superseded |
| `SOTA Coding Agents Benchmarks` | Coding-agent benchmark/comparison studies |

**Metadata Tabs:**

| Tab | One row per | Purpose |
| --- | --- | --- |
| `Dictionary` | radar column | Position, which tabs it applies to, value type, separator, description |
| `Vocabulary` | controlled term | Term, definition, and its ontology mapping |
| `Standards` | external standard | The standards the vocabulary draws on |

The controlled vocabulary is backed by four standards where a genuine match exists: [EDAM ontology](http://edamontology.org/topic_3071) (`Data management` branch, primary), [NIST AI RMF 1.0](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf) (secondary axis), ACM Computing Classification System 2012, and Schema.org. Terms with no ontology mapping are project-local.

`data/json/` is a machine-readable mirror (one JSON file per tab) that agents can read and edit directly; `xlsx_to_json.py` and `json_to_xlsx.py` keep it and the xlsx in sync. Any added/removed/edited row clears that row's `Verified By`/`Last Verified` — a human re-approving content they never saw would be a false claim. Old values aren't lost; they're recoverable from git history on the json files.

### GitOps Implementation

git/GitHub pull requests are the versioning, review, and audit system for `data/json/*.json`.

**Roles**
- **Contributor** — submits an updated xlsx as a PR. Does not fill in `Verified By`/`Last Verified`: they propose content, they don't attest to having checked it.
- **Curator** — verifies the content, fills in `Verified By`/`Last Verified`, approves, and merges. Required PR reviewer for `data/json/**` (`.github/CODEOWNERS` + branch protection).
- **Admin** (`.github/RADAR-ADMINS`) — must approve any PR that deletes a row with no match anywhere else in the workbook.

**GitHub repository role to grant**

| Project role | GitHub role | Notes |
| --- | --- | --- |
| Contributor | **Write** | Needed to push a branch and open a PR from inside the repo. Cannot merge without a curator's approval. |
| Curator | **Write** | Minimum for an approval to count toward branch protection — a review from a Read or Triage user does not. Also the minimum for a CODEOWNERS entry to be requestable. |
| Admin | **Admin** | Only Admin can edit branch protection or bypass a failing required check. |

Do **not** grant Maintain: over Write it adds only repository-metadata powers (description, topics, wikis, merge settings, Pages, Copilot exclusions) that neither role needs, and no review or merge capability that Write lacks.

Write permits merging once branch protection is satisfied (approvals + required checks); it cannot bypass. Admin can merge regardless while `enforce_admins` is `false`.

Repository roles alone do not separate "may approve" from "may merge" — both are Write, so a contributor could merge their own PR once a curator approves it. To make that a real boundary, set branch protection `restrictions` (currently unset) naming who may push/merge to `main`. Until then it is convention only.

Once a second Write collaborator exists, set `enforce_admins: true` on `main`. It is currently `false` so that a solo admin isn't locked out by rules requiring a second person; that exemption stops being necessary — and becomes a standing hole — as soon as someone else can review.

**Source of truth**: `data/json/*.json`, fully git-tracked. Git history (`git log`/`git blame`) is the audit trail. The xlsx is committed alongside it and kept in sync by targeted cell writes, so it is already correct when a PR merges — there is no separate publish step.

**Row identity**: each row's `ID` (not `Resource Name`) is the key matched across runs, so renaming a resource doesn't look like a delete-plus-add. `Added/Edited By` records who or what last touched a row's content — self-declared by default, overwritten with a trusted identity (e.g. `github.actor`) when a script run supplies `--actor`.

**Workflow**
1. Bootstrap (one time): `xlsx_to_json.py` converts the xlsx into `data/json/*.json`.
2. Ongoing edits go through a PR — either directly to the json, or by uploading a changed xlsx (`xlsx-to-json.yml` converts the upload into the same kind of json diff, stamping `Added/Edited By` with the uploader's GitHub handle).
3. Any added/removed/edited row has `Verified By`/`Last Verified` cleared automatically as part of that conversion. A row that disappears with no match in any other sheet requires an admin's approval (`deletion-authorization.yml`, a required status check) before the PR can merge.
4. Curator verifies the content, fills in `Verified By`/`Last Verified` by re-uploading the xlsx to the same PR branch, then approves. A fresh, fully-supplied verification survives the sync; the contributor stays recorded in `Added/Edited By`.
5. Curator merges.

No git CLI or branch-pushing is required of contributors or curators — every step is available through GitHub's native web UI (edit-in-browser, drag-and-drop upload, "Approve" button, "Merge" button).

### Status

| Component | Status |
| --- | --- |
| `src/scripts/radar_sync_common.py` | Done |
| `src/scripts/tech_radar_analysis.py` | Done — see `data/reports/workbook_analysis.md` |
| Workbook metadata tabs (`Dictionary`/`Vocabulary`/`Standards`) | Done — 18 columns (incl. `ID`, `Added/Edited By`), 76 vocabulary terms, 4 standards |
| `.github/CODEOWNERS` for `data/json/**` | Done — names `@pbuendia` |
| Branch protection on `main` | Done — PR + 1 code-owner approval required; `Deletion authorization / check` required; admin bypass allowed |
| `src/scripts/xlsx_to_json.py` | Done — schema-driven; auto-assigns `ID`; validates workbook structure before converting; detects cross-sheet row moves vs. deletions; `--actor` stamps `Added/Edited By` |
| `src/scripts/json_to_xlsx.py` | Done — rebuilds the entire workbook from `data/json/` |
| `src/scripts/check_deletion_authorization.py` | Done — blocks a PR that deletes a row unless an admin approved it |
| GitHub Action — xlsx upload → json diff (`xlsx-to-json.yml`) | Done, confirmed on a real PR |
| GitHub Action — deletion authorization (`deletion-authorization.yml`) | Done, confirmed on a real PR |
| GitHub Action — publish (`workflow_dispatch` → Release) | Dropped — the xlsx is already in sync at merge time, so nothing needs regenerating |
| GitHub Action — stamp `Verified By` from the approval | Not built. Blocked: the Actions app cannot be granted `bypass_pull_request_allowances`, so a workflow cannot push to `main`. Curators fill the fields manually instead (step 4 above) |
| Developer/user documentation | This file + `scripts-guide.md` + `user_guides/README.md` |

**Known gap**: no check yet enforces the verification rule against a hand-edited JSON commit (that `Verified By` is never non-empty while its content hash differs from the verified baseline) — today it's enforced only when `xlsx_to_json.py` itself does the conversion.

## Agentic Process to update the VT Radar

Not implemented. No design decisions made yet.

## Agentic Assessment Landscape Framework (ALAF)

Not implemented. No design decisions made yet.