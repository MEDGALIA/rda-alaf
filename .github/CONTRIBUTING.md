# Contributing to ALAF

Thanks for your interest in contributing to the Agentic Landscape Assessment
Framework. This project is early-stage and welcomes issues, discussion, and
pull requests from the research data community.

By participating, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md).

## Ways to contribute

- **Report a bug or gap** — open a [GitHub issue](https://github.com/MEDGALIA/ALAF/issues)
  describing what's wrong or missing. For the VT Radar knowledge base, include
  which row/term is affected and why.
- **Propose a knowledge base change** — see [Updating the VT Radar knowledge base](#updating-the-vt-radar-knowledge-base)
  below.
- **Improve tooling or docs** — see [Development setup](#development-setup).
- **Discuss framework direction** — since the RDA Working Group has not yet
  been formed, larger design questions are best raised as an issue first,
  before investing time in a PR.

## Ground rules

- Every change goes through a pull request — no direct pushes to `main`.
- Keep PRs focused; unrelated changes make review harder and slow everyone down.
- Write commit messages that explain *why*, not just *what*.
- Don't introduce secrets, credentials, or personal data into the repository.
- Sign off on the [Code of Conduct](CODE_OF_CONDUCT.md) — be respectful and
  assume good faith.

## Updating the VT Radar knowledge base

The knowledge base lives in [`data/VANTAGE-Technology-Radar.xlsx`](data/VANTAGE-Technology-Radar.xlsx)
and is mirrored to `data/json/` for machine consumption. This repo uses a
GitOps workflow, described in full in
[`developer_guides/implementation-plan.md`](developer_guides/implementation-plan.md):

1. Edit the xlsx directly (add/update rows, or controlled-vocabulary terms in
   the `Vocabulary` tab).
2. Run the sync script to regenerate `data/json/`:
   ```powershell
   .\.venv\Scripts\python src\scripts\xlsx_to_json.py
   ```
   Use `--fresh` only after a schema (column) change — see
   [`developer_guides/scripts-guide.md`](developer_guides/scripts-guide.md) for why.
3. Optionally regenerate the coverage report to sanity-check your change:
   ```powershell
   .\.venv\Scripts\python src\scripts\tech_radar_analysis.py
   ```
4. Commit both the xlsx and the regenerated `data/json/` files together, and
   open a pull request. Changes under `data/json/**` require review from a
   curator (see [`.github/CODEOWNERS`](.github/CODEOWNERS)) before merging.

Do not hand-edit files under `data/json/` — they're generated. Edit the xlsx
and re-run the sync script instead.

## Development setup

```powershell
python -m venv .venv
.\.venv\Scripts\pip install -r src\scripts\requirements.txt
```

See [`developer_guides/scripts-guide.md`](developer_guides/scripts-guide.md)
for what each script in `src/scripts/` does and how to run it.

## Pull request checklist

- [ ] Change is scoped to one concern
- [ ] If you touched the xlsx: `data/json/` was regenerated and committed alongside it
- [ ] If you touched a script's behavior: `developer_guides/` docs updated to match
- [ ] No unrelated formatting/whitespace churn

## License

ALAF software is licensed under the [BSD 3-Clause License](LICENSE). The
VT Radar knowledge base and other datasets are licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). By contributing,
you agree that your contributions will be licensed under the same terms as
the files you're modifying.
