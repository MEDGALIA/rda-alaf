"""Render Markdown files into elegant, self-contained, styled HTML pages.

Usage:
    python md_to_html.py <input_dir> <output_dir>

Every ``*.md`` file found (non-recursively) in ``input_dir`` is rendered to
an HTML page of the same name in ``output_dir``, wrapped in a clean,
print-friendly template with syntax-highlighted code blocks, styled tables,
and support for both light and dark viewing.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import markdown2
from pygments.formatters import HtmlFormatter

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
{pygments_css}
{base_css}
</style>
</head>
<body>
<article class="doc">
{body}
</article>
</body>
</html>
"""

BASE_CSS = """
:root {
  --bg: #ffffff;
  --fg: #1b1f24;
  --muted: #57606a;
  --border: #d8dee4;
  --accent: #2f6feb;
  --code-bg: #f6f8fa;
  --heading: #0b3d91;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #0d1117;
    --fg: #e6edf3;
    --muted: #9198a1;
    --border: #30363d;
    --accent: #6cb6ff;
    --code-bg: #161b22;
    --heading: #79c0ff;
  }
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: var(--bg);
  color: var(--fg);
  font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
  line-height: 1.65;
}
.doc {
  max-width: 860px;
  margin: 0 auto;
  padding: 3rem 1.5rem 6rem;
}
h1, h2, h3, h4 {
  color: var(--heading);
  font-weight: 650;
  line-height: 1.3;
  margin-top: 2.2em;
  margin-bottom: 0.6em;
}
h1 { font-size: 2.1rem; border-bottom: 1px solid var(--border); padding-bottom: 0.4em; margin-top: 0; }
h2 { font-size: 1.5rem; border-bottom: 1px solid var(--border); padding-bottom: 0.3em; }
h3 { font-size: 1.2rem; }
h4 { font-size: 1.05rem; color: var(--fg); }
p, ul, ol { margin: 0.9em 0; }
ul, ol { padding-left: 1.6em; }
li { margin: 0.3em 0; }
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
code {
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 0.15em 0.4em;
  font-size: 0.88em;
  font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
}
pre {
  background: var(--code-bg);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1em 1.2em;
  overflow-x: auto;
}
pre code { background: none; border: none; padding: 0; }
/* Override Pygments' hardcoded light background so highlighted code blocks
   follow the page theme instead of staying light-gray in dark mode. */
.codehilite {
  background: var(--code-bg) !important;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1em 1.2em;
  margin: 1em 0;
  overflow-x: auto;
}
.codehilite pre {
  background: none;
  border: none;
  padding: 0;
  margin: 0;
  overflow: visible;
}
blockquote {
  margin: 1em 0;
  padding: 0.2em 1em;
  border-left: 4px solid var(--accent);
  color: var(--muted);
  background: var(--code-bg);
  border-radius: 0 6px 6px 0;
}
table {
  border-collapse: collapse;
  width: 100%;
  margin: 1.2em 0;
  font-size: 0.95em;
}
th, td {
  border: 1px solid var(--border);
  padding: 0.5em 0.8em;
  text-align: left;
}
th { background: var(--code-bg); }
tr:nth-child(even) td { background: color-mix(in srgb, var(--code-bg) 45%, transparent); }
hr { border: none; border-top: 1px solid var(--border); margin: 2.5em 0; }
img { max-width: 100%; border-radius: 6px; }
"""

MD_EXTRAS = [
    "fenced-code-blocks",
    "tables",
    "header-ids",
    "toc",
    "strike",
    "task_list",
    "footnotes",
    "code-friendly",
]


def render_file(md_path: Path, output_dir: Path) -> Path:
    text = md_path.read_text(encoding="utf-8")
    body = markdown2.markdown(text, extras=MD_EXTRAS)

    pygments_css = HtmlFormatter(style="default").get_style_defs(".codehilite")
    title = md_path.stem.replace("_", " ").replace("-", " ")

    html = PAGE_TEMPLATE.format(
        title=title,
        pygments_css=pygments_css,
        base_css=BASE_CSS,
        body=body,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / (md_path.stem + ".html")
    output_path.write_text(html, encoding="utf-8")
    return output_path


def convert_directory(input_dir: Path, output_dir: Path) -> list[Path]:
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    md_files = sorted(input_dir.glob("*.md"))
    if not md_files:
        print(f"No .md files found in {input_dir}", file=sys.stderr)
        return []

    return [render_file(md_path, output_dir) for md_path in md_files]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert all Markdown files in a directory to styled HTML pages."
    )
    parser.add_argument("input_dir", type=Path, help="Directory containing .md files")
    parser.add_argument("output_dir", type=Path, help="Directory to write .html files to")
    args = parser.parse_args()

    written = convert_directory(args.input_dir, args.output_dir)
    for path in written:
        print(f"Wrote {path}")


if __name__ == "__main__":
    main()
