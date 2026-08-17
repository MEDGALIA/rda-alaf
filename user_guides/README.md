# How to convert a Word document to Markdown

This guide walks through running the `docx_to_md.py` script to turn a `.docx` file into a `.md` file.

## 1. One-time setup

From the repository root, create a virtual environment and install the required packages:

```powershell
python -m venv .venv
.\.venv\Scripts\pip install -r src\scripts\requirements.txt
```

You only need to do this once. If `.venv\` already exists, skip straight to step 2.

## 2. Run the script

```powershell
.\.venv\Scripts\python src\scripts\docx_to_md.py "drafts\your-file.docx"
```

This creates `drafts\your-file.md` next to the original `.docx`. Any images inside the document are saved into a `your-file_images\` folder alongside it, and linked automatically from the Markdown.

### Choosing a different output location

```powershell
.\.venv\Scripts\python src\scripts\docx_to_md.py "drafts\your-file.docx" -o "drafts\renamed-output.md"
```

### Skipping image extraction

```powershell
.\.venv\Scripts\python src\scripts\docx_to_md.py "drafts\your-file.docx" --no-images
```

### Naming the images folder

By default, images are extracted to `<output-name>_images\`. To use a fixed, shorter folder name instead (recommended, so re-running the script doesn't create a new folder if you rename the `.docx`):

```powershell
.\.venv\Scripts\python src\scripts\docx_to_md.py "drafts\your-file.docx" --images-dir draft_images
```

## Example

```powershell
.\.venv\Scripts\python src\scripts\docx_to_md.py "drafts\VANTAGE WG - Statement of Work (SoW) (2).docx" --images-dir draft_images
```

produces `drafts\VANTAGE WG - Statement of Work (SoW) (2).md`, with images saved to `drafts\draft_images\`.

## Troubleshooting

- **"No module named mammoth"** — the virtual environment isn't activated or wasn't installed into. Re-run the setup command in step 1.
- **Warnings printed about "Unrecognised paragraph/run style"** — these are informational only (usually custom Word styles like `Title` or footnote references) and don't affect the converted output.
- **Formatting looks off** — Word documents with unusual custom styles may need a style map; see [developer_guides/scripts-guide.md](../developer_guides/scripts-guide.md) for how to extend the script.
