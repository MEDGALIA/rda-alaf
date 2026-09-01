# Scripts — Developer Guide

This guide covers the scripts in [`src/scripts/`](../src/scripts/):

| Script | Purpose |
| --- | --- |
| `docx_to_md.py` | Converts a Word `.docx` file into Markdown |
| `md_to_html.py` | Renders a directory of `.md` files into styled, self-contained HTML pages |
| `radar_sync_common.py` | Shared helpers for the VT Radar xlsx ⇄ JSON tooling (not run directly) |
| `tech_radar_analysis.py` | Read-only analysis of the VT Radar workbook (data quality + vocabulary coverage) |
| `xlsx_to_json.py` | Converts the VT Radar workbook into `data/json/` (schema + one file per data sheet) |
| `json_to_xlsx.py` | Rebuilds the VT Radar workbook from `data/json/` — the mirror of `xlsx_to_json.py` |
| `sync_gdrive_mirror.py` | Pushes the workbook to a Google Sheet, for viewing conditional formatting GitHub doesn't render |

All are plain Python 3 scripts with no project framework dependency — they can be run standalone or imported as modules. The VT Radar scripts implement the plan in [`implementation-plan.md`](implementation-plan.md) — see that doc for the overall design and current build status.

## Environment setup

The repo uses a local virtual environment at `.venv/` (already excluded from git via `.gitignore`).

```powershell
python -m venv .venv
.\.venv\Scripts\pip install -r src\scripts\requirements.txt
```

Pinned versions live in [`src/scripts/requirements.txt`](../src/scripts/requirements.txt).

| Package | Used by | Role |
| --- | --- | --- |
| `mammoth` | `docx_to_md.py` | Reads `.docx` XML and emits semantic HTML (headings, lists, tables, bold/italic, embedded images) |
| `markdownify` | `docx_to_md.py` | Converts the intermediate HTML into Markdown (ATX-style headings, `-` bullets) |
| `markdown2` | `md_to_html.py` | Converts Markdown back into HTML with GitHub-style extras (tables, fenced code, footnotes, task lists, TOC) |
| `pygments` | `md_to_html.py` | Generates the CSS for syntax-highlighted code blocks |
| `openpyxl` | `radar_sync_common.py`, `tech_radar_analysis.py`, `xlsx_to_json.py` | Reads/writes `.xlsx` workbooks with native typed cells (dates come back as `datetime`, not serial numbers) |
| `google-auth` | `sync_gdrive_mirror.py` | Authenticates as the Google Cloud service account |
| `google-api-python-client` | `sync_gdrive_mirror.py` | Calls the Google Drive API |

## `docx_to_md.py`

```powershell
.\.venv\Scripts\python src\scripts\docx_to_md.py "<input>.docx" -o "<output>.md"
```

**Arguments**

- `input` (positional) — path to the source `.docx`
- `-o / --output` — destination `.md` path (defaults to the input path with a `.md` extension)
- `--no-images` — skip extracting embedded images
- `--images-dir NAME` — folder name for extracted images (defaults to `<output-stem>_images`). Pass a fixed name (e.g. `draft_images`) when a file may be re-converted under a different output name, so re-runs reuse the same folder instead of orphaning the old one.

**How it works**

1. `mammoth.convert_to_html()` parses the `.docx` and maps Word styles onto HTML tags. Any embedded images are streamed through a custom handler (`_make_image_handler`) that writes them to an `<output-stem>_images/` folder next to the output file and rewrites the `<img src>` to a relative path.
2. `markdownify()` converts the resulting HTML into Markdown.
3. `_clean_markdown()` strips trailing whitespace and collapses runs of 3+ blank lines introduced by the conversion.

Conversion warnings (e.g. unrecognised Word paragraph/run styles) are printed to stderr but do not stop the conversion — they're informational only and don't affect output quality in practice.

**Extending it**: to change how a particular Word style is mapped (e.g. custom heading styles), pass a `style_map` string to `mammoth.convert_to_html(..., style_map=...)` — see the [mammoth style-mapping docs](https://github.com/mwilliamson/python-mammoth#writing-style-maps).

## `md_to_html.py`

```powershell
.\.venv\Scripts\python src\scripts\md_to_html.py developer_guides developer_guides_html
```

**Arguments**

- `input_dir` (positional) — directory to scan for `*.md` files (non-recursive)
- `output_dir` (positional) — directory to write the matching `*.html` files to

**How it works**

1. Every `*.md` file directly inside `input_dir` is read and rendered with `markdown2.markdown()`, using extras for fenced code blocks, tables, header IDs, a table of contents, strikethrough, task lists, and footnotes.
2. Each page is wrapped in `PAGE_TEMPLATE`, a self-contained HTML shell with an inlined stylesheet (`BASE_CSS`) plus the Pygments-generated syntax-highlighting CSS. There are no external asset dependencies — each output `.html` file works standalone, offline, and respects the reader's OS light/dark preference via `prefers-color-scheme`.
3. Output filenames mirror the input stem (`guide.md` → `guide.html`).

**Extending it**: styling lives entirely in the `BASE_CSS` string — edit it directly to adjust fonts, colors, or layout. To render recursively or add a landing/index page listing all converted guides, extend `convert_directory()`.

## `radar_sync_common.py`

Not a standalone script — a shared helper module imported by the VT Radar tooling (`tech_radar_analysis.py`, `xlsx_to_json.py`, `json_to_xlsx.py`). Lives in `src/scripts/` so it's importable via a relative import (`from radar_sync_common import ...`) from sibling scripts.

**What it provides**

- `slugify(header)` — turns an xlsx column header into a JSON-safe key, e.g. `"Notes / Key Takeaways"` → `notes_key_takeaways`.
- `content_hash(record)` — SHA-256 over a record's fields, excluding `id`/`verified_by`/`last_verified`/`_content_hash`. Used to detect whether a record's substantive content changed since a stored baseline.
- `new_id(existing_ids)` — short 8-hex-char UUID, collision-checked against a set of IDs already in use. Used by `xlsx_to_json.py` to assign a row's `ID` the first time it sees that row with the cell blank.
- `cell_display_value(value)` — renders an `openpyxl` cell value (str/number/`datetime`/`None`) as a JSON-safe string, converting dates to ISO `YYYY-MM-DD`.
- `split_multi_value(text, separator)` — splits a delimited cell into trimmed, de-duplicated terms. Tolerates `,` as well as the configured separator, since rows written before the `;` standardization used commas.
- `load_workbook_schema(wb)` — reads the `Dictionary`/`Vocabulary`/`Standards` tabs into `{"standards": [...], "columns": [...]}`, with each column's vocabulary terms nested underneath it. **This is the single source of truth** for which columns are controlled vocabularies and how their cells split.
- `load_sheet_json(path)` / `save_sheet_json(path, data)` — read/write a JSON file with consistent formatting (`indent=2`, trailing newline, LF). `load_sheet_json` returns `None` if the file doesn't exist yet.
- `iter_header(ws)` — yields `(column_letter, header_text)` for each non-empty cell in row 1.
- `row_is_empty(ws, row_idx, columns)` — `True` if every cell in that row (across the given columns) is blank.
- `METADATA_SHEETS` / `CONTROLLED_TYPES` — the metadata tab names, and the `Value Type` values that mean "controlled vocabulary".

## The workbook's three metadata tabs

`data/VANTAGE-Technology-Radar.xlsx` holds three normalized metadata tabs alongside the data tabs. They are the schema, not records, and `xlsx_to_json.py` turns them into a single hierarchical `data/json/dictionary.json`.

| Tab | One row per | Columns |
| --- | --- | --- |
| `Dictionary` | radar column | `Position`, `Column Name`, `Applies To`, `Value Type`, `Separator`, `Description` |
| `Vocabulary` | controlled term | `Column Name`, `Term`, `Definition`, `Ontology`, `Ontology ID`, `Ontology URL` |
| `Standards` | external standard | `Standard ID`, `Name`, `Version`, `URL`, `Notes` |

`Value Type` drives the whole pipeline: `id`, `free_text`, `date`, `person`, `version`, `controlled_single`, `controlled_multi`. A `controlled_multi` column becomes a real JSON array, split on its `Separator` — so adding a multi-value column needs no code change, only a Dictionary row. `id` is special-cased only by `xlsx_to_json.py`'s auto-assignment step (see below) — everywhere else it's treated like any other plain-text column.

`Vocabulary.Ontology` references `Standards.Standard ID`. Four standards are declared: **EDAM** (primary controlled vocabulary — open ontology with permanent per-term URIs), **NIST AI RMF 1.0** (secondary axis for AI-trustworthiness framing; document-based, so no per-term URIs), **ACM Computing Classification System 2012** (general CS taxonomy, cited by category-path text), and **Schema.org** (CreativeWork/SoftwareApplication hierarchy, for `Resource Type`). Terms with no ontology are deliberately project-local rather than force-mapped onto a mismatched external term.

> **Careful:** NIST's `Fair (harmful bias managed)` (algorithmic non-discrimination) is unrelated to EDAM's `FAIR data` (Findable/Accessible/Interoperable/Reusable). They share a word and nothing else — the `Standards` tab notes carry this warning too.

## `xlsx_to_json.py`

```powershell
.\.venv\Scripts\python src\scripts\xlsx_to_json.py [--xlsx PATH] [--out-dir data/json] [--fresh] [--actor NAME]
```

Converts the workbook into `data/json/`: `dictionary.json` (the hierarchical schema, from the three metadata tabs) plus one file per data sheet.

**Arguments**

- `--xlsx PATH` — source workbook (default: `data/VANTAGE-Technology-Radar.xlsx`)
- `--out-dir PATH` — JSON destination (default: `data/json`)
- `--fresh` — rebuild the verification baseline from the workbook, ignoring existing JSON. **Required after any schema change** (see below).
- `--actor NAME` — overwrites `Added/Edited By` (in both the JSON and the xlsx cell) on any row whose content changed in this run, e.g. `--actor "@$GITHUB_ACTOR"`. Omitted for local runs, which leave the field as self-declared.

**Row identity and the verification rule**

Each sheet's first column, `ID`, is the natural key matching a row across runs — a system-generated value independent of `Resource Name`, so renaming a resource doesn't look like deleting one row and adding an unrelated new one. Any row found with a blank `ID` cell gets one assigned automatically and written back into the xlsx before conversion runs (`assign_missing_ids()`) — a curator never fills this in by hand, except when intentionally moving a row to a different sheet, where the ID should be copied along with the rest of the row.

For every row, a `_content_hash` is stored over its substantive fields (excluding `id`, `verified_by`, `last_verified`, `added_edited_by`). On the next run:

- hash unchanged, verification fields unchanged → carried through untouched (a true no-op);
- content and/or verification fields changed, and the new `Verified By`/`Last Verified` were freshly and fully supplied in this same edit → trusted as a deliberate re-verification;
- otherwise → both fields are **cleared**, because a human hasn't reviewed this version. The cleared row is named on stdout.

This applies the same way whether it's the row's *content* that changed, or only its verification fields (e.g. a curator filling in `Last Verified` on a row whose `Verified By` was already set, with nothing else touched) — both are treated as edits needing a fresh-verification decision.

Old values are never lost — `data/json/` is git-tracked, so `git log`/`git blame` recovers them.

> **Gotcha worth knowing:** adding or removing a *column* changes every row's hash, so a schema change looks identical to "somebody edited all rows" and would wipe every verification. **After any schema change, run with `--fresh`**, which re-establishes the baseline instead of diffing against differently-shaped JSON. `--fresh` also removes any need to delete files by hand.

**Structure validation**: before converting anything, `validate_structure()` checks that every data sheet's columns exactly match what `Dictionary` declares for it — same headers, same order. A mismatch (missing column, unexpected column, wrong order) raises immediately and **no JSON is written at all**, so a malformed upload never partially converts.

**Moves vs. deletions**: a row whose `ID` is missing from one sheet is checked against every other data sheet's current contents. Found elsewhere (e.g. moved from `Knowledgebase` to `Deprecated`, with the `ID` copied along) → reported as a move. Found nowhere → reported as a deletion. This is **detection only** — the script doesn't block a true deletion, since it has no notion of who's running it or whether they're authorized; enforcing "only an admin-merged PR may delete a row" is a GitHub Action-side check, not yet built (see `drafts/VANTAGE-Tech-Radar-Sync-Plan.md`'s Approval System section).

## `json_to_xlsx.py`

```powershell
.\.venv\Scripts\python src\scripts\json_to_xlsx.py [--json-dir data/json] [--out PATH]
```

The mirror of `xlsx_to_json.py`: rebuilds the **entire** workbook from `data/json/*.json` from scratch — every data sheet plus `Dictionary`/`Vocabulary`/`Standards` — rather than patching cells in place. `data/json/` is the source of truth in the GitOps design (see `implementation-plan.md`); the xlsx is a generated artifact for human consumption, published as a GitHub Release.

**Arguments**

- `--json-dir PATH` — source JSON directory (default: `data/json`)
- `--out PATH` — destination xlsx (default: `data/VANTAGE-Technology-Radar.xlsx`)

**What's guaranteed, what isn't**: content round-trips exactly — every field of every record, and the full `Dictionary`/`Vocabulary`/`Standards` schema, verified field-by-field against the source JSON. Cosmetic details (column widths, frozen header row, bold headers) are sane regenerated defaults, not a clone of any hand-tweaked formatting a curator may have applied to a previous xlsx.

## `tech_radar_analysis.py`

```powershell
.\.venv\Scripts\python src\scripts\tech_radar_analysis.py [--xlsx PATH] [--out data/reports/workbook_analysis.md]
```

Read-only analysis of the workbook — never opens it in write mode, and asserts the file's bytes are unchanged before vs. after the scan.

**Arguments**

- `--xlsx PATH` — workbook to scan (default: `data/VANTAGE-Technology-Radar.xlsx`)
- `--out PATH` — Markdown report destination (default: `data/reports/workbook_analysis.md`)

**What it reports**

- **Row counts and cell anomalies**, per sheet — empty rows as contiguous ranges, plus type/shape checks keyed off the header: name-like columns flagged if numeric/date; date columns flagged if not a real date cell; `Version` flagged if it *is* a date; `URL` flagged if it doesn't start with `http(s)://`.
- **Column coverage** — columns in data tabs missing from `Dictionary`, and documented columns no tab actually has.
- **Vocabulary coverage** — per controlled column: terms used but absent from `Vocabulary`, and documented terms never used. Driven by `Value Type`, so free-text columns are skipped — without that, `Relevance to Research Cyberinfrastructure` (prose sentences by design) would report ~30 bogus "undocumented terms".
- **Missing controlled values** — populated rows with an empty controlled-vocabulary cell, which is usually an oversight rather than a deliberate "not applicable".
- **Ontology coverage** — which vocabulary terms are backed by a declared standard and which aren't.
- **Review candidates** — near-duplicate term pairs (one term's words a subset of another's, e.g. `Retrieval` vs `Retrieval Agents`) that were deliberately *not* auto-merged, since collapsing them is a semantic judgment rather than a spelling fix.

No "corrected" value is ever suggested — deciding what a bad cell *should* say is a human judgment call, not something to guess at for a real WG record. See [`implementation-plan.md`](implementation-plan.md) for why this script is report-only by design.

**Output**: a Markdown report (`data/reports/workbook_analysis.md` by default) with per-sheet summary counts (total/empty/populated/anomalous rows) followed by a table of every anomaly found.

## `sync_gdrive_mirror.py`

```powershell
.\.venv\Scripts\python src\scripts\sync_gdrive_mirror.py --xlsx data\VANTAGE-Technology-Radar.xlsx --key-file PATH
```

Pushes the workbook to a Google Sheet — see `drafts/VT-Radar-GDrive-Mirror-Plan.md` for the design. `main` stays the source of truth; this only pushes, never reads the Sheet back.

**Arguments**

- `--xlsx PATH` — source workbook (default: `data/VANTAGE-Technology-Radar.xlsx`)
- `--key-file PATH` — service-account JSON key file. Read from a file, never a CLI value or env var directly, so it never appears in shell history or process listings.
- `--config PATH` — RADAR-CONFIG path (default: `.github/RADAR-CONFIG`)

Target Sheet is `gdrive_file_id` in `.github/RADAR-CONFIG` — not a secret; access is controlled by the Sheet's sharing settings. `files.update()` replaces the Sheet's entire content with the latest xlsx, converted via `mimeType: application/vnd.google-apps.spreadsheet`.

## Adding a new document to convert

1. Manually copy the `.docx` into `drafts/` (gitignored — safe for working files), then manually run `docx_to_md.py` to produce the `.md`. Nothing watches this folder — both steps are run by hand, on demand.
2. To publish developer-facing documentation, place the `.md` source in `developer_guides/`, then manually re-run `md_to_html.py developer_guides developer_guides_html` to regenerate the HTML.
3. To publish curator/end-user-facing documentation (e.g. `user_guides/VT_RADAR.md`, "how to submit an xlsx update"), place the `.md` source in `user_guides/`, then manually re-run `md_to_html.py user_guides user_guides_html`.
