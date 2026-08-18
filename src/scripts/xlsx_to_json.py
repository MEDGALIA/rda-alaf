"""Convert the VT Radar workbook into JSON: one file per data sheet, plus a
hierarchical schema file built from the metadata tabs.

Bootstraps data/json/ from data/VANTAGE-Technology-Radar.xlsx, and is re-run
whenever the xlsx changes (by hand, or by the GitHub Action that reacts to an
uploaded xlsx in a PR).

The Dictionary/Vocabulary/Standards tabs are the schema, not records: they
become data/json/dictionary.json, with each column's controlled-vocabulary
terms (and their ontology mappings) nested underneath it. That schema also
drives the conversion -- a column declared `controlled_multi` becomes a real
JSON array, split on the separator the Dictionary tab specifies, rather than
the script hardcoding column names.

Row identity: each sheet's first column (e.g. "Resource Name") is the natural
key used to match a row across runs. If an existing row's content changed
since the last run, its Verified By/Last Verified are cleared -- UNLESS a
human filled in both fields in that same xlsx edit, which is treated as a
deliberate re-verification and kept as-is: editing a row and re-confirming
Verified By in the same pass is exactly how a human is expected to (re-)verify
it. A brand-new row (no known prior baseline at all) always has its
verification trusted as-is, for the same reason. Rows whose key no longer
appears in the xlsx are dropped (recoverable from git history, since
data/json/ is tracked).

When a row's verification is cleared, the corresponding xlsx cells are also
blanked (the script opens the workbook a second time, in write mode, only for
this). Without that, a cleared row's still-populated xlsx cell would silently
leak back into the JSON the next time that row's content changes again,
un-clearing something that was correctly cleared before -- this is otherwise
a normal read-only conversion, this is the one exception.

NOTE: adding or removing a column changes every row's content hash, so a
schema change makes this look like "every row was edited" and would clear all
verification for rows nobody actually touched. After any schema change, re-run
with --fresh, which rebuilds the baseline from the workbook instead of diffing
against the previous (differently-shaped) JSON.

Usage:
    python xlsx_to_json.py [--xlsx PATH] [--out-dir data/json] [--fresh]
"""

from __future__ import annotations

import argparse
from pathlib import Path

import openpyxl

from radar_sync_common import (
    METADATA_SHEETS,
    cell_display_value,
    content_hash,
    iter_header,
    load_sheet_json,
    load_workbook_schema,
    row_is_empty,
    save_sheet_json,
    slugify,
    split_multi_value,
)

DEFAULT_XLSX = Path("data/VANTAGE-Technology-Radar.xlsx")
DEFAULT_OUT_DIR = Path("data/json")

VERIFICATION_FIELDS = ("verified_by", "last_verified")


def sheet_to_records(ws, schema: dict) -> tuple[list[dict], list[str], dict[str, int]]:
    """Read a data sheet into records, using the schema to type each column.

    Also returns {natural_key: row_idx}, so the caller can write cleared
    verification back to the xlsx (see convert()) -- otherwise a cleared
    row's stale, never-blanked cell would leak back into the JSON the next
    time that row's content changes again.
    """
    columns = list(iter_header(ws))
    by_name = {c["name"]: c for c in schema["columns"]}

    records = []
    row_index_by_key = {}
    for row_idx in range(2, ws.max_row + 1):
        if row_is_empty(ws, row_idx, columns):
            continue
        record = {}
        for col_letter, header in columns:
            raw = ws[f"{col_letter}{row_idx}"].value
            spec = by_name.get(header)
            if spec and spec["value_type"] == "controlled_multi":
                record[slugify(header)] = split_multi_value(raw, spec["separator"] or ";")
            else:
                record[slugify(header)] = cell_display_value(raw)
        records.append(record)
        row_index_by_key[record[slugify(columns[0][1])]] = row_idx

    return records, [slugify(h) for _c, h in columns], row_index_by_key


def merge_with_previous(
    records: list[dict], previous: dict | None, key_field: str
) -> tuple[list[dict], list[str], list[str]]:
    """Clear verification on new/changed rows; report what changed."""
    prev_by_key = {r[key_field]: r for r in (previous or {}).get("records", [])} if previous else {}

    cleared, kept_keys = [], set()
    merged = []
    for record in records:
        key = record[key_field]
        kept_keys.add(key)
        if not any(f in record for f in VERIFICATION_FIELDS):
            merged.append(record)
            continue

        prev_record = prev_by_key.get(key)
        new_hash = content_hash(record)

        if prev_record is not None and prev_record.get("_content_hash") == new_hash:
            # Unchanged since last run -- carry the prior verification through.
            record["verified_by"] = prev_record.get("verified_by", record.get("verified_by", ""))
            record["last_verified"] = prev_record.get("last_verified", record.get("last_verified", ""))
            record["_content_hash"] = new_hash
            merged.append(record)
            continue

        # Content differs from the known baseline (or there is none -- a brand-new
        # row). Was verification *freshly supplied in this same edit*, as opposed
        # to just sitting there non-blank from a previous, now-stale verification?
        # Comparing against the value last recorded in the JSON (not merely
        # checking "is it non-blank now") is what tells the two apart: editing an
        # unrelated field while Verified By/Last Verified happen to still show a
        # name and date from before is NOT a re-verification, even though both
        # fields are technically filled in.
        prev_verified_by = prev_record.get("verified_by", "") if prev_record else ""
        prev_last_verified = prev_record.get("last_verified", "") if prev_record else ""
        verified_by, last_verified = record.get("verified_by", ""), record.get("last_verified", "")
        fully_supplied = bool(verified_by) and bool(last_verified)
        freshly_touched = verified_by != prev_verified_by or last_verified != prev_last_verified

        if fully_supplied and freshly_touched:
            # A human supplied (or changed) both fields in this same edit -- trust
            # it as a deliberate re-verification. This is the whole point of xlsx
            # being the human's verification channel.
            pass
        else:
            # Not a fresh, deliberate re-verification -- force fully blank.
            # Forcing blank even when it was already blank matters: without it, a
            # stale non-blank xlsx cell that was never physically cleared (see the
            # write-back step in convert()) would leak back in here and silently
            # un-clear a row that was correctly cleared before.
            was_verified = bool(verified_by or last_verified)
            record["verified_by"] = ""
            record["last_verified"] = ""
            if was_verified:
                cleared.append(key)
        record["_content_hash"] = new_hash
        merged.append(record)

    removed = sorted(k for k in prev_by_key if k not in kept_keys)
    return merged, cleared, removed


def convert(xlsx_path: Path, out_dir: Path, fresh: bool = False) -> None:
    wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    if fresh:
        print("--fresh: rebuilding the baseline from the workbook, ignoring existing JSON")

    schema = load_workbook_schema(wb)
    schema_path = out_dir / "dictionary.json"
    save_sheet_json(schema_path, schema)
    controlled = sum(1 for c in schema["columns"] if c["terms"])
    print(
        f"schema: {len(schema['columns'])} columns "
        f"({controlled} with vocabularies), {len(schema['standards'])} standards -> {schema_path}"
    )

    # (sheet_name, row_idx, field) for cells where the JSON says "blank" but
    # the xlsx cell itself isn't -- must be blanked too, or a later run that
    # re-reads the xlsx fresh will let the stale value leak back into the
    # JSON, silently un-clearing a row that was correctly cleared before.
    to_blank: list[tuple[str, int, str]] = []

    for sheet_name in wb.sheetnames:
        if sheet_name in METADATA_SHEETS:
            continue
        ws = wb[sheet_name]
        records, columns, row_index = sheet_to_records(ws, schema)
        if not columns:
            continue
        key_field = columns[0]

        out_path = out_dir / f"{slugify(sheet_name)}.json"
        previous = None if fresh else load_sheet_json(out_path)
        merged, cleared, removed = merge_with_previous(records, previous, key_field)

        header_letters = {slugify(h): c for c, h in iter_header(ws)}
        for record in merged:
            row_idx = row_index[record[key_field]]
            for field in VERIFICATION_FIELDS:
                if field not in record or record[field]:
                    continue
                letter = header_letters.get(field)
                if letter and ws[f"{letter}{row_idx}"].value not in (None, ""):
                    to_blank.append((sheet_name, row_idx, field))

        save_sheet_json(out_path, {"sheet_name": sheet_name, "columns": columns, "records": merged})

        print(f"{sheet_name}: wrote {len(merged)} records to {out_path}")
        for key in cleared:
            print(f"  cleared verification: {key!r} (content changed)")
        for key in removed:
            print(f"  removed (no longer in xlsx): {key!r}")

    wb.close()

    if to_blank:
        wb_write = openpyxl.load_workbook(xlsx_path)  # formulas preserved
        for sheet_name, row_idx, field in to_blank:
            ws = wb_write[sheet_name]
            header_letters = {slugify(h): c for c, h in iter_header(ws)}
            cell = ws[f"{header_letters[field]}{row_idx}"]
            cell.value = None  # NOTE: cell(..., value=None) is a no-op; must assign .value directly
        wb_write.save(xlsx_path)
        print(f"blanked {len(to_blank)} stale verification cell(s) directly in the xlsx (kept in sync with the JSON)")
        for sheet_name, row_idx, field in to_blank:
            print(f"  {sheet_name} row {row_idx}: {field}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert the VT Radar xlsx into JSON.")
    parser.add_argument("--xlsx", type=Path, default=DEFAULT_XLSX)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument(
        "--fresh", action="store_true",
        help="Rebuild the baseline from the workbook, ignoring existing JSON. Use after any "
             "column/schema change, which otherwise looks like every row was edited.",
    )
    args = parser.parse_args()

    convert(args.xlsx, args.out_dir, fresh=args.fresh)


if __name__ == "__main__":
    main()
