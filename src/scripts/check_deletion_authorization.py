"""Required status check: a PR that deletes a VT Radar row needs an admin's
approval before it can merge.

Compares data/json/*.json between a PR's base and head to find any row ID
that disappears from *every* data sheet (a true deletion, not a move to
another sheet -- xlsx_to_json.py already reports the same distinction on
stdout during conversion; this recomputes it independently since it runs
against the JSON diff in a PR, not against an xlsx being converted).

If no true deletion is found, the check passes immediately -- ordinary edits
never need an admin's attention. If one is found, the check only passes if
the PR already carries an APPROVED review from someone on the admin list
(.github/RADAR-ADMINS). This deliberately checks *approval*, not *merge*:
a required status check runs before the Merge button is even clickable, so
it has no way to know who will eventually click it -- only who has already
reviewed. (An earlier version of this design tried to key off who merges,
which turned out not to be checkable pre-merge at all.)

A repo admin can always merge past a failing required check via branch
protection's "include administrators" bypass -- this check doesn't need to
special-case a solo admin proposing their own deletion, the same way the
existing required-review rule doesn't either.

Usage:
    python check_deletion_authorization.py --base-dir DIR --head-dir DIR
        --admins-file .github/RADAR-ADMINS --repo owner/repo --pr-number N
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def load_ids(json_dir: Path) -> dict[str, set[str]]:
    """{sheet_slug: {id, ...}} for every data sheet json in a directory."""
    ids_by_sheet: dict[str, set[str]] = {}
    for path in json_dir.glob("*.json"):
        if path.stem == "dictionary":
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        ids_by_sheet[path.stem] = {r["id"] for r in data.get("records", []) if r.get("id")}
    return ids_by_sheet


def find_true_deletions(base_dir: Path, head_dir: Path) -> list[str]:
    """IDs present in the base but missing from every sheet in the head."""
    base_ids = load_ids(base_dir)
    head_ids = load_ids(head_dir)
    all_head_ids = set().union(*head_ids.values()) if head_ids else set()

    deleted = []
    for sheet, ids in base_ids.items():
        for row_id in ids - head_ids.get(sheet, set()):
            if row_id not in all_head_ids:
                deleted.append(row_id)
    return sorted(deleted)


def load_admins(admins_file: Path) -> set[str]:
    admins = set()
    for line in admins_file.read_text(encoding="utf-8").splitlines():
        line = line.split("#", 1)[0].strip()
        if line:
            admins.add(line)
    return admins


def approved_by_admin(repo: str, pr_number: int, admins: set[str]) -> tuple[bool, list[str]]:
    """Whether the PR has an APPROVED review from someone on the admin list.

    Uses the gh CLI (preinstalled on GitHub-hosted runners, and already the
    tool used elsewhere in this project to inspect repo/PR state) rather
    than adding a new HTTP dependency just for this one check.
    """
    result = subprocess.run(
        ["gh", "pr", "view", str(pr_number), "--repo", repo, "--json", "reviews"],
        capture_output=True, text=True, check=True,
    )
    reviews = json.loads(result.stdout)["reviews"]
    approvers = [r["author"]["login"] for r in reviews if r["state"] == "APPROVED"]
    admin_approvers = [a for a in approvers if a in admins]
    return bool(admin_approvers), admin_approvers


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-dir", type=Path, required=True)
    parser.add_argument("--head-dir", type=Path, required=True)
    parser.add_argument("--admins-file", type=Path, required=True)
    parser.add_argument("--repo", required=True, help="owner/repo")
    parser.add_argument("--pr-number", type=int, required=True)
    args = parser.parse_args()

    deleted = find_true_deletions(args.base_dir, args.head_dir)
    if not deleted:
        print("No row deletions in this PR -- nothing to authorize.")
        return

    print(f"True deletion(s) detected (no match in any sheet): {deleted}")
    admins = load_admins(args.admins_file)
    ok, admin_approvers = approved_by_admin(args.repo, args.pr_number, admins)
    if ok:
        print(f"Authorized -- approved by admin(s): {admin_approvers}")
        return

    print(
        f"BLOCKED: this PR deletes {len(deleted)} row(s) with no move to another sheet, "
        f"and has no approving review from anyone on the admin list ({sorted(admins)}). "
        "An admin must approve this PR before it can merge.",
        file=sys.stderr,
    )
    sys.exit(1)


if __name__ == "__main__":
    main()
