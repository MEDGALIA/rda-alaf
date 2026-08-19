# Submitting an update to the VT Radar

This guide is for curators updating the VANTAGE Technology Radar (VT Radar) knowledge base by editing the spreadsheet — no `git` command line, no coding. Everything happens through GitHub's website.

## What you're editing

`data/VANTAGE-Technology-Radar.xlsx` is the human-facing copy of the knowledge base — a normal Excel workbook with three data tabs (`Knowledgebase`, `Deprecated`, `SOTA Coding Agents Benchmarks`) plus three tabs that document the schema and controlled vocabulary (`Dictionary`, `Vocabulary`, `Standards`). A machine-readable mirror lives in `data/json/` and is regenerated automatically from your xlsx — you never need to touch it.

## Step by step

1. **Download and edit.** Get the current workbook from `data/VANTAGE-Technology-Radar.xlsx` in the repo, edit it in Excel (or another real spreadsheet app), save.
2. **Go to the file on github.com.** Navigate to `data/` in the repository, click `VANTAGE-Technology-Radar.xlsx`.
3. **Upload your edited copy.** Use "Add file" → "Upload files" (or the upload option on the file page), drag in your edited file with the same filename so it replaces the old one.
4. **Commit as a new branch.** GitHub will offer to commit. Choose *"Create a new branch for this commit and start a pull request"* — it auto-names the branch for you, and opens a pull request (PR). You don't need to understand what a branch is; just follow the prompt.
5. **Wait for the automatic sync.** Once your PR is open, GitHub automatically converts your xlsx into the machine-readable JSON files and adds that as a second commit on your PR. You don't trigger this yourself — it just happens.
6. **A curator reviews and approves.** Someone with review rights reads the diff and approves the PR.
7. **A publisher merges.** Once merged, your changes are live.

## Rules the sync follows automatically

You don't need to do anything special for these — they just happen when your file is processed:

- **`Verified By` / `Last Verified` get cleared automatically** whenever a row's content changes and you didn't fill in *both* fields yourself in the same edit. This is deliberate: a "verified" stamp should only survive if a human actually looked at the current version. If you're updating a row and want it to stay marked verified, fill in **both** `Verified By` and `Last Verified` yourself as part of that same edit.
- **Every row has a hidden `ID` column** (column A on each data tab) that you generally shouldn't touch. It's how the sync recognizes "this is the same row as before" even if you rename it, and it gets assigned automatically for any new row you add — just leave it blank and it'll be filled in for you.
- **Moving a row between tabs** (e.g. a resource that's now deprecated): copy the *entire* row — including its `ID` — from `Knowledgebase` into `Deprecated`, then delete it from `Knowledgebase`. As long as the `ID` comes along, the sync recognizes it as a move, not a deletion, and its history is preserved.
- **Deleting a row outright** (no move, it's just gone) is detected and reported, but today isn't blocked by anything automatic — a repo admin still needs to be the one to actually merge a PR that removes a row with no match anywhere else. If you're not sure whether something should be deleted vs. moved to `Deprecated`, ask first.
- **Your file's structure is checked before anything else happens.** If a column got renamed, removed, or reordered by accident, the sync refuses to run at all rather than guessing — you'll need to fix the structure and re-upload. Stick to editing cell *values*, not column headers or their order, unless you're deliberately proposing a schema change (in which case, flag it — that's a bigger conversation than a normal content update).
- **`Added/Edited By`** records who or what last touched a row. Fill in your own name when you edit a row by hand; an AI agent fills in its own name. If you upload the xlsx via GitHub, this gets set to your GitHub handle automatically on any row you actually changed — you don't need to fill it in yourself in that case.

## Questions or something looks wrong

Open an issue on the repository, or reach out to a curator directly — don't guess at fixing a structural problem yourself.
