"""Shared Markdown to HTML conversion utilities."""

import html
import re


def inline_format(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+?)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*(.+?)\*\*|__(.+?)__", lambda m: f"<strong>{m.group(1) or m.group(2)}</strong>", text)
    text = re.sub(r"\*(.+?)\*|_(.+?)_", lambda m: f"<em>{m.group(1) or m.group(2)}</em>", text)
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r"<a href=\"\2\">\1</a>", text)
    return text


def convert_markdown_to_html(markdown_text: str) -> str:
    lines = markdown_text.splitlines()
    html_lines = []
    open_list = None
    open_paragraph = False
    in_code_block = False
    code_block_lines = []

    def close_paragraph():
        nonlocal open_paragraph
        if open_paragraph:
            html_lines.append('</p>')
            open_paragraph = False

    def close_list():
        nonlocal open_list
        if open_list == 'ul':
            html_lines.append('</ul>')
        elif open_list == 'ol':
            html_lines.append('</ol>')
        open_list = None

    def close_code_block():
        nonlocal in_code_block, code_block_lines
        if in_code_block:
            html_lines.append('<pre><code>')
            html_lines.extend(html.escape(line) for line in code_block_lines)
            html_lines.append('</code></pre>')
            code_block_lines = []
            in_code_block = False

    for raw_line in lines:
        line = raw_line.rstrip('\n')
        if line.startswith('```'):
            if in_code_block:
                close_code_block()
                continue
            close_paragraph()
            close_list()
            in_code_block = True
            code_block_lines = []
            continue

        if in_code_block:
            code_block_lines.append(line)
            continue

        if not line.strip():
            close_paragraph()
            close_list()
            continue

        heading_match = re.match(r'^(#{1,6})\s+(.*)$', line)
        if heading_match:
            close_paragraph()
            close_list()
            level = len(heading_match.group(1))
            heading_text = inline_format(heading_match.group(2).strip())
            html_lines.append(f'<h{level}>{heading_text}</h{level}>')
            continue

        hr_match = re.match(r'^(?:\*{3,}|-{3,}|_{3,})\s*$', line)
        if hr_match:
            close_paragraph()
            close_list()
            html_lines.append('<hr />')
            continue

        quote_match = re.match(r'^>\s?(.*)$', line)
        if quote_match:
            close_paragraph()
            close_list()
            quote_text = inline_format(quote_match.group(1).strip())
            html_lines.append(f'<blockquote>{quote_text}</blockquote>')
            continue

        list_match = re.match(r'^([-+*])\s+(.*)$', line)
        ordered_match = re.match(r'^(\d+)\.\s+(.*)$', line)
        if list_match or ordered_match:
            close_paragraph()
            tag = 'ul' if list_match else 'ol'
            item_text = inline_format((list_match or ordered_match).group(2).strip())
            if open_list != tag:
                close_list()
                html_lines.append(f'<{tag}>')
                open_list = tag
            html_lines.append(f'  <li>{item_text}</li>')
            continue

        if open_list:
            close_list()

        if not open_paragraph:
            html_lines.append('<p>')
            open_paragraph = True

        html_lines.append(inline_format(line.strip()))

    close_code_block()
    close_paragraph()
    close_list()

    return '\n'.join(html_lines)


def build_html_document(body_html: str, title: str = 'Markdown Conversion') -> str:
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)}</title>
  <style>
    body {{ font-family: Inter, system-ui, Arial, sans-serif; background: #f4f7fb; color: #202124; margin: 0; padding: 2rem; max-width: 900px; }}
    h1, h2, h3, h4, h5, h6 {{ margin-top: 1.4rem; }}
    p {{ margin: 0 0 1rem; }}
    pre {{ background: #1e1e1e; color: #f8f8f2; padding: 1rem; overflow-x: auto; border-radius: 8px; }}
    code {{ background: #e8eaed; padding: 0.2rem 0.4rem; border-radius: 5px; }}
    blockquote {{ color: #555; border-left: 4px solid #dfe1e5; padding-left: 1rem; margin: 1rem 0; }}
    ul, ol {{ margin: 0 0 1rem 1.5rem; }}
    hr {{ border: none; border-top: 1px solid #dfe1e5; margin: 1.5rem 0; }}
    a {{ color: #1a73e8; text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
  </style>
</head>
<body>
{body_html}
</body>
</html>'''
