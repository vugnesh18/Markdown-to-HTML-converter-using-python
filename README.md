Name: BHANU VIGNESH
InternID:CITS1394
# Markdown to HTML Converter

A simple Python command-line app that converts Markdown files into HTML.

## Usage

Convert a single Markdown file:

```bash
python markdown_to_html.py input.md
```

This writes `input.html` next to the original file.

Convert a file to a specific output path:

```bash
python markdown_to_html.py input.md output.html
```

Convert all Markdown files in a directory:

```bash
python markdown_to_html.py docs/ output/
```

## Features

- Basic heading support (`#`, `##`, ...)
- Paragraphs, lists, blockquotes, horizontal rules
- Inline bold, italic, code spans, and links
- Fenced code block support
- Self-contained, no external dependencies required

## GUI Version

Run the graphical interface with:

```bash
python markdown_to_html_ui.py
```

Then:
- paste or load Markdown on the left
- click **Convert** to generate HTML
- preview in your browser
- save the result to an `.html` file
