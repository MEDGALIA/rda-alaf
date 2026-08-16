"""Placeholder script for synchronizing VT-Radar.xlsx with a JSON representation.

Usage:
    python scripts/sync_vt_radar.py --input VT-Radar.xlsx --output vt_radar.json
"""

import argparse


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync VT-Radar.xlsx knowledge base to JSON."
    )
    parser.add_argument("--input", required=True, help="Path to VT-Radar.xlsx")
    parser.add_argument("--output", required=True, help="Path for output JSON file")
    args = parser.parse_args()

    print(f"[sync_vt_radar] input={args.input!r}  output={args.output!r}")
    raise NotImplementedError("sync_vt_radar is not yet implemented.")


if __name__ == "__main__":
    main()
