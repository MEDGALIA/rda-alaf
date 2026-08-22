# Submitting an update to the VT Radar

This guide is for **contributors** updating the VANTAGE Technology Radar (VT Radar) knowledge base by editing the spreadsheet — no `git` command line, no coding. Everything happens through GitHub's website. If you are the curator reviewing a submission, see [For the curator](#for-the-curator) at the end.

## What you're editing

`data/VANTAGE-Technology-Radar.xlsx` is the human-facing copy of the knowledge base — a normal Excel workbook with three data tabs (`Knowledgebase`, `Deprecated`, `SOTA Coding Agents Benchmarks`) plus three tabs that document the schema and controlled vocabulary (`Dictionary`, `Vocabulary`, `Standards`). A machine-readable mirror lives in `data/json/` and is regenerated automatically from your xlsx — you never need to touch it.

## Step by step

1. **Download and edit.** Get the current workbook from `data/VANTAGE-Technology-Radar.xlsx` in the repo, edit it in Excel (or another real spreadsheet app), save.
2. **Go to the file on github.com.** Navigate to `data/` in the repository, click `VANTAGE-Technology-Radar.xlsx`.
3. **Upload your edited copy.** Use "Add file" → "Upload files" (or the upload option on the file page), drag in your edited file with the same filename so it replaces the old one.
4. **Commit as a new branch.** GitHub will offer to commit. Choose *"Create a new branch for this commit and start a pull request"* — it auto-names the branch for you, and opens a pull request (PR). You don't need to understand what a branch is; just follow the prompt.
5. **Wait for the automatic sync.** Once your PR is open, GitHub automatically converts your xlsx into the machine-readable JSON files and adds that as a second commit on your PR. You don't trigger this yourself — it just happens.
6. **The curator verifies and approves.** They check the resources themselves, fill in who verified them, and approve.
7. **The curator merges.** Once merged, your changes are live.

## Rules the sync follows automatically

You don't need to do anything special for these — they just happen when your file is processed:

- **Leave `Verified By` and `Last Verified` alone.** They record that a curator personally checked the resource — not that the row was edited. Whenever you change a row's content, both fields are cleared automatically, and the curator fills them back in after checking. Don't fill them in yourself, and don't put someone else's name in them.
- **Every row has an `ID` column** (column A on each data tab) that you shouldn't touch. It's how the sync recognizes "this is the same row as before" even if you rename it, and it gets assigned automatically for any new row you add — just leave it blank and it'll be filled in for you.
- **Moving a row between tabs** (e.g. a resource that's now deprecated): copy the *entire* row — including its `ID` — from `Knowledgebase` into `Deprecated`, then delete it from `Knowledgebase`. As long as the `ID` comes along, the sync recognizes it as a move, not a deletion, and its history is preserved.
- **Deleting a row outright** (no move, it's just gone) blocks the PR until a repo admin approves it. If you're not sure whether something should be deleted or moved to `Deprecated`, ask first.
- **Your file's structure is checked before anything else happens.** If a column got renamed, removed, or reordered by accident, the sync refuses to run at all rather than guessing — you'll need to fix the structure and re-upload. Stick to editing cell *values*, not column headers or their order, unless you're deliberately proposing a schema change (in which case, flag it — that's a bigger conversation than a normal content update).
- **`Added/Edited By`** records who last touched a row. When you upload via GitHub it's set to your GitHub handle automatically on any row you actually changed — you don't need to fill it in.

## For the curator

Approving a PR does **not** fill in `Verified By`/`Last Verified` — nothing writes them for you. To record a verification:

1. Download the xlsx **from the PR branch**, not from `main`.
2. Open the resources and actually check them.
3. Fill in **both** `Verified By` (your name) and `Last Verified` (today) on the rows you checked. One without the other is treated as invalid and cleared.
4. Re-upload that xlsx to the **same PR branch**. The sync keeps your verification and leaves `Added/Edited By` pointing at the contributor.
5. **Then** approve, and merge.

Approve last: any push to the branch — including the automatic sync — cancels an earlier approval, so approving before step 4 will silently come undone.

## Questions or something looks wrong

Open an issue on the repository, or reach out to a curator directly — don't guess at fixing a structural problem yourself.
