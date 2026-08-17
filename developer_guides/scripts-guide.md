# Scripts — Developer Guide

This guide covers the scripts in [`src/scripts/`](../src/scripts/):

| Script | Purpose |
| --- | --- |
| `docx_to_md.py` | Converts a Word `.docx` file into Markdown |
| `md_to_html.py` | Renders a directory of `.md` files into styled, self-contained HTML pages |
| `radar_sync_common.py` | Shared helpers for the VT Radar xlsx ⇄ JSON tooling (not run directly) |
| `tech_radar_quality_report.py` | Read-only data-quality scan of the VT Radar workbook |

All are plain Python 3 scripts with no project framework dependency — they can be run standalone or imported as modules. The VT Radar scripts (`radar_sync_common.py`, `tech_radar_quality_report.py`, and more to come) implement the plan in [`implementation-plan.md`](implementation-plan.md) — see that doc for the overall design and current build status.

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
| `openpyxl` | `radar_sync_common.py`, `tech_radar_quality_report.py` | Reads/writes `.xlsx` workbooks with native typed cells (dates come back as `datetime`, not serial numbers) |

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

Not a standalone script — a shared helper module imported by the VT Radar sync tooling (`tech_radar_quality_report.py` today; `xlsx_to_json.py`/`json_to_xlsx.py` once written). Lives in `src/scripts/` so it's importable via a relative import (`from radar_sync_common import ...`) from sibling scripts run with `src/scripts/` as the working directory.

**What it provides**

- `slugify(header)` — turns an xlsx column header into a JSON-safe key, e.g. `"Notes / Key Takeaways"` → `notes_key_takeaways`.
- `content_hash(record)` — SHA-256 over a record's fields, excluding `id`/`verified_by`/`last_verified`/`_content_hash`. Used to detect whether a record's substantive content changed since a stored baseline.
- `new_id(existing_ids)` — short 8-hex-char UUID, collision-checked against a set of IDs already in use.
- `cell_display_value(value)` — renders an `openpyxl` cell value (str/number/`datetime`/`None`) as a JSON-safe string, converting dates to ISO `YYYY-MM-DD`.
- `load_sheet_json(path)` / `save_sheet_json(path, data)` — read/write a sheet's JSON file with consistent formatting (`indent=2`, trailing newline). `load_sheet_json` returns `None` if the file doesn't exist yet.
- `iter_header(ws)` — yields `(column_letter, header_text)` for each non-empty cell in row 1.
- `row_is_empty(ws, row_idx, columns)` — `True` if every cell in that row (across the given columns) is blank.

## `tech_radar_quality_report.py`

```powershell
.\.venv\Scripts\python src\scripts\tech_radar_quality_report.py [--xlsx PATH] [--out drafts/workbook_errors.md]
```

Read-only scan of the VT Radar workbook (`data/VANTAGE-Technology-Radar.xlsx` by default) — it never opens the file in write mode, and asserts the file's bytes are byte-for-byte unchanged before vs. after the scan runs.

**Arguments**

- `--xlsx PATH` — workbook to scan (default: `data/VANTAGE-Technology-Radar.xlsx`)
- `--out PATH` — Markdown report destination (default: `drafts/workbook_errors.md`)

**What it flags, per sheet**

- **Empty rows** — rows with no content in any cell, reported as contiguous ranges rather than one line per row.
- **Type/shape anomalies**, via simple per-column heuristics keyed off the header text (unrecognized headers are skipped):
  - `Verified By` / `Source Organization` / `Resource Name` — flagged if numeric or a real date (clearly not a name/org/title).
  - `Last Verified` / `Deprecation Date` — flagged if *not* a real date-typed cell.
  - `Version` — flagged if it *is* a real date-typed cell (the inverse check — a date serial sitting where a version string belongs is exactly the anomaly already seen in this workbook).
  - `URL` — flagged if non-empty and doesn't start with `http://` or `https://`.

No "corrected" value is ever suggested — deciding what a bad cell *should* say is a human judgment call, not something to guess at for a real WG record. See [`implementation-plan.md`](implementation-plan.md) for why this script is report-only by design.

**Output**: a Markdown report (`drafts/workbook_errors.md` by default) with per-sheet summary counts (total/empty/populated/anomalous rows) followed by a table of every anomaly found.

## Adding a new document to convert

1. Manually copy the `.docx` into `drafts/` (gitignored — safe for working files), then manually run `docx_to_md.py` to produce the `.md`. Nothing watches this folder — both steps are run by hand, on demand.
2. To publish developer-facing documentation, place the `.md` source in `developer_guides/`, then manually re-run `md_to_html.py developer_guides developer_guides_html` to regenerate the HTML.
