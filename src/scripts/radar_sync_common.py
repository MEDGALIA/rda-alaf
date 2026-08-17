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

RESERVED_KEYS = {"id", "verified_by", "last_verified", "_content_hash"}


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
