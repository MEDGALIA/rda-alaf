"""Convert a Word (.docx) document into a Markdown (.md) file.

Usage:
    python docx_to_md.py <input.docx> [-o OUTPUT.md] [--images-dir NAME]

Pipeline: mammoth turns the .docx into semantic HTML (respecting heading
styles, lists, tables, bold/italic), then markdownify turns that HTML into
Markdown. Embedded images are extracted to an "<output-name>_images/"
folder (or a custom folder name passed via --images-dir) next to the
output file and linked from the Markdown.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import mammoth
from markdownify import markdownify


def _make_image_handler(images_dir: Path, md_relative_dir: str):
    """Return a mammoth image handler that saves images to disk."""
    counter = {"n": 0}

    def convert_image(image):
        counter["n"] += 1
        extension = (image.content_type or "image/png").split("/")[-1]
        extension = "jpg" if extension == "jpeg" else extension
        filename = f"image_{counter['n']:03d}.{extension}"
        images_dir.mkdir(parents=True, exist_ok=True)
        with image.open() as image_bytes:
            (images_dir / filename).write_bytes(image_bytes.read())
        return {"src": f"{md_relative_dir}/{filename}"}

    return mammoth.images.img_element(convert_image)


def _clean_markdown(text: str) -> str:
    """Collapse excess blank lines and trailing whitespace left by the converters."""
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def convert(
    docx_path: Path,
    output_path: Path,
    extract_images: bool = True,
    images_dir_name: str | None = None,
) -> Path:
    if not docx_path.exists():
        raise FileNotFoundError(f"Input file not found: {docx_path}")

    images_dir_name = images_dir_name or f"{output_path.stem}_images"
    images_dir = output_path.parent / images_dir_name

    convert_kwargs = {}
    if extract_images:
        convert_kwargs["convert_image"] = _make_image_handler(images_dir, images_dir_name)

    with docx_path.open("rb") as docx_file:
        result = mammoth.convert_to_html(docx_file, **convert_kwargs)

    for warning in result.messages:
        print(f"warning: {warning.message}", file=sys.stderr)

    markdown = markdownify(result.value, heading_style="ATX", bullets="-")
    markdown = _clean_markdown(markdown)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")

    if images_dir.exists() and not any(images_dir.iterdir()):
        images_dir.rmdir()

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a .docx file to Markdown.")
    parser.add_argument("input", type=Path, help="Path to the source .docx file")
    parser.add_argument(
        "-o", "--output", type=Path, default=None,
        help="Path to the output .md file (defaults to same name, .md extension, same folder)",
    )
    parser.add_argument(
        "--no-images", action="store_true",
        help="Skip extracting embedded images",
    )
    parser.add_argument(
        "--images-dir", type=str, default=None,
        help="Folder name for extracted images (defaults to '<output-name>_images')",
    )
    args = parser.parse_args()

    output_path = args.output or args.input.with_suffix(".md")
    result_path = convert(
        args.input,
        output_path,
        extract_images=not args.no_images,
        images_dir_name=args.images_dir,
    )
    print(f"Wrote {result_path}")


if __name__ == "__main__":
    main()
