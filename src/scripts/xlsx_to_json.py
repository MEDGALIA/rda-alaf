"""Convert the VT Radar workbook into one JSON file per sheet.

Bootstraps data/json/*.json from data/VANTAGE-Technology-Radar.xlsx, and is
re-run whenever the xlsx changes (by hand, or by the future GitHub Action
that reacts to an uploaded xlsx in a PR).

Row identity: each sheet's first column (e.g. "Resource Name") is used as
the natural key to match a row across runs -- there's no separate ID column
in this workbook. If a row's content changed since the last run (or it's
new), its Verified By/Last Verified are cleared, since a human hasn't seen
the new content yet. Rows whose key no longer appears in the xlsx are
dropped from the JSON (recoverable from git history, since data/json/ is
tracked).

Usage:
    python xlsx_to_json.py [--xlsx PATH] [--out-dir data/json]
"""

from __future__ import annotations

import argparse
from pathlib import Path

import openpyxl

from radar_sync_common import (
    cell_display_value,
    content_hash,
    iter_header,
    load_sheet_json,
    row_is_empty,
    save_sheet_json,
    slugify,
)

DEFAULT_XLSX = Path("data/VANTAGE-Technology-Radar.xlsx")
DEFAULT_OUT_DIR = Path("data/json")

VERIFICATION_FIELDS = ("verified_by", "last_verified")


def sheet_to_records(ws) -> tuple[list[dict], list[str]]:
    columns = list(iter_header(ws))
    key_col = columns[0][0]  # first column's letter is the natural-key column

    records = []
    for row_idx in range(2, ws.max_row + 1):
        if row_is_empty(ws, row_idx, columns):
            continue
        record = {slugify(header): cell_display_value(ws[f"{col}{row_idx}"].value) for col, header in columns}
        records.append(record)

    return records, [slugify(h) for _c, h in columns]


def merge_with_previous(records: list[dict], previous: dict | None, key_field: str) -> tuple[list[dict], list[str], list[str]]:
    """Clear verification on new/changed rows; report what changed."""
    prev_by_key = {r[key_field]: r for r in (previous or {}).get("records", [])} if previous else {}

    cleared, kept_keys = [], set()
    merged = []
    for record in records:
        key = record[key_field]
        kept_keys.add(key)
        has_verification = any(f in record for f in VERIFICATION_FIELDS)
        if not has_verification:
            merged.append(record)
            continue

        prev_record = prev_by_key.get(key)
        new_hash = content_hash(record)
        if prev_record is not None and prev_record.get("_content_hash") == new_hash:
            # Unchanged since last run -- carry the prior verification through.
            record["verified_by"] = prev_record.get("verified_by", record.get("verified_by", ""))
            record["last_verified"] = prev_record.get("last_verified", record.get("last_verified", ""))
        elif prev_record is not None and (prev_record.get("verified_by") or prev_record.get("last_verified")):
            # Changed, and it used to be verified -- clear it, a human hasn't seen this version.
            record["verified_by"] = ""
            record["last_verified"] = ""
            cleared.append(key)
        record["_content_hash"] = new_hash
        merged.append(record)

    removed = sorted(k for k in prev_by_key if k not in kept_keys)
    return merged, cleared, removed


def convert(xlsx_path: Path, out_dir: Path) -> None:
    wb = openpyxl.load_workbook(xlsx_path, data_only=True)

    for sheet_name in wb.sheetnames:
        records, columns = sheet_to_records(wb[sheet_name])
        if not columns:
            continue
        key_field = columns[0]

        out_path = out_dir / f"{slugify(sheet_name)}.json"
        previous = load_sheet_json(out_path)
        merged, cleared, removed = merge_with_previous(records, previous, key_field)

        save_sheet_json(out_path, {"sheet_name": sheet_name, "columns": columns, "records": merged})

        print(f"{sheet_name}: wrote {len(merged)} records to {out_path}")
        for key in cleared:
            print(f"  cleared verification: {key!r} (content changed)")
        for key in removed:
            print(f"  removed (no longer in xlsx): {key!r}")

    wb.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert the VT Radar xlsx into per-sheet JSON files.")
    parser.add_argument("--xlsx", type=Path, default=DEFAULT_XLSX)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    convert(args.xlsx, args.out_dir)


if __name__ == "__main__":
    main()
