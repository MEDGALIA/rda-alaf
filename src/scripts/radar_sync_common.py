"""Shared helpers for the VANTAGE Technology Radar xlsx <-> JSON sync tooling.

Used by tech_radar_quality_report.py, xlsx_to_json.py, and json_to_xlsx.py.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import re
import uuid
from pathlib import Path

RESERVED_KEYS = {"id", "verified_by", "last_verified", "added_edited_by", "_content_hash"}

# Metadata tabs describe the schema/vocabulary rather than holding radar
# records, so the record-oriented conversion skips them.
METADATA_SHEETS = ("Dictionary", "Vocabulary", "Standards")

CONTROLLED_TYPES = ("controlled_single", "controlled_multi")


def slugify(header: str) -> str:
    """'Notes / Key Takeaways' -> 'notes_key_takeaways'"""
    slug = re.sub(r"[^0-9a-zA-Z]+", "_", header.strip().lower())
    return slug.strip("_")


def content_hash(record: dict) -> str:
    """Hash of a record's substantive fields (excludes id/verification metadata)."""
    payload = {k: v for k, v in record.items() if k not in RESERVED_KEYS}
    encoded = json.dumps(payload, sort_keys=True, default=str)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def new_id(existing_ids: set[str]) -> str:
    """Short UUID, collision-checked against IDs already used in the sheet."""
    while True:
        candidate = uuid.uuid4().hex[:8]
        if candidate not in existing_ids:
            existing_ids.add(candidate)
            return candidate


def cell_display_value(value) -> str:
    """Render an openpyxl cell value (str/number/datetime/None) as a JSON-safe string."""
    if value is None:
        return ""
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.date().isoformat() if isinstance(value, datetime.datetime) else value.isoformat()
    return str(value)


def load_sheet_json(path: Path) -> dict | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_sheet_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def iter_header(ws):
    """Yield (column_letter, header_text) for each non-empty cell in row 1."""
    for cell in ws[1]:
        if cell.value is not None and str(cell.value).strip():
            yield cell.column_letter, str(cell.value).strip()


def row_is_empty(ws, row_idx: int, columns) -> bool:
    for col_letter, _header in columns:
        value = ws[f"{col_letter}{row_idx}"].value
        if value is not None and str(value).strip() != "":
            return False
    return True


def split_multi_value(text, separator: str = ";") -> list[str]:
    """Split a delimited cell into trimmed, de-duplicated terms.

    Accepts ',' as well as the configured separator: older rows predate the
    switch to ';', and tolerating both keeps them readable either way.
    """
    if text is None or not str(text).strip():
        return []
    pattern = f"[{re.escape(separator)},]"
    out, seen = [], set()
    for part in re.split(pattern, str(text)):
        term = part.strip()
        if term and term.lower() not in seen:
            seen.add(term.lower())
            out.append(term)
    return out


def _table_rows(ws) -> list[dict]:
    """Read a headed metadata tab into a list of {header: value} dicts."""
    headers = [str(c.value).strip() if c.value else "" for c in ws[1]]
    rows = []
    for row in ws.iter_rows(min_row=2):
        values = [cell_display_value(c.value) for c in row]
        if not any(v for v in values):
            continue
        rows.append({h: v for h, v in zip(headers, values) if h})
    return rows


def load_workbook_schema(wb) -> dict:
    """Build the schema from the Dictionary/Vocabulary/Standards tabs.

    Returns {"standards": [...], "columns": [...]} where each column carries
    its terms nested underneath it. This is the single source of truth for
    which columns are controlled vocabularies and how multi-value cells split.
    """
    standards = [
        {
            "id": r.get("Standard ID", ""),
            "name": r.get("Name", ""),
            "version": r.get("Version", ""),
            "url": r.get("URL", ""),
            "notes": r.get("Notes", ""),
        }
        for r in _table_rows(wb["Standards"])
    ]

    terms_by_column: dict[str, list[dict]] = {}
    for r in _table_rows(wb["Vocabulary"]):
        terms_by_column.setdefault(r.get("Column Name", ""), []).append(
            {
                "name": r.get("Term", ""),
                "definition": r.get("Definition", ""),
                "ontology": r.get("Ontology", ""),
                "ontology_id": r.get("Ontology ID", ""),
                "ontology_url": r.get("Ontology URL", ""),
            }
        )

    columns = []
    for r in _table_rows(wb["Dictionary"]):
        name = r.get("Column Name", "")
        position = r.get("Position", "")
        columns.append(
            {
                "position": int(float(position)) if position else None,
                "name": name,
                "key": slugify(name),
                "applies_to": split_multi_value(r.get("Applies To", "")),
                "value_type": r.get("Value Type", ""),
                "separator": r.get("Separator", "") or None,
                "description": r.get("Description", ""),
                "terms": terms_by_column.get(name, []),
            }
        )

    return {"standards": standards, "columns": columns}
