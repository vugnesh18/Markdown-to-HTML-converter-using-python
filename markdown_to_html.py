"""Markdown to HTML converter command-line app."""

import argparse
import pathlib
import sys

from converter import build_html_document, convert_markdown_to_html


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Convert Markdown file(s) to HTML.')
    parser.add_argument('input', help='Markdown input file or directory')
    parser.add_argument('output', nargs='?', help='Output HTML file or directory')
    parser.add_argument('--title', default='Markdown Conversion', help='HTML document title')
    parser.add_argument('--overwrite', action='store_true', help='Overwrite output files without prompt')
    return parser.parse_args()


def convert_file(input_path: pathlib.Path, output_path: pathlib.Path, title: str) -> None:
    markdown_text = input_path.read_text(encoding='utf-8')
    body_html = convert_markdown_to_html(markdown_text)
    html_text = build_html_document(body_html, title=title)
    output_path.write_text(html_text, encoding='utf-8')
    print(f'Converted: {input_path} -> {output_path}')


def main() -> int:
    args = parse_args()
    input_path = pathlib.Path(args.input)
    output_path = pathlib.Path(args.output) if args.output else None

    if input_path.is_dir():
        files = list(sorted(input_path.glob('*.md')))
        if not files:
            print(f'No Markdown files found in directory: {input_path}', file=sys.stderr)
            return 1
        if output_path is None:
            print('When converting a directory, specify an output directory.', file=sys.stderr)
            return 1
        output_path.mkdir(parents=True, exist_ok=True)
        for md_file in files:
            out_file = output_path / (md_file.stem + '.html')
            convert_file(md_file, out_file, title=args.title)
        return 0

    if not input_path.exists():
        print(f'Input file not found: {input_path}', file=sys.stderr)
        return 1

    if output_path is None:
        output_path = input_path.with_suffix('.html')
    elif output_path.exists() and output_path.is_dir():
        output_path = output_path / (input_path.stem + '.html')

    if output_path.exists() and not args.overwrite:
        print(f'Output file already exists: {output_path}', file=sys.stderr)
        print('Use --overwrite to replace it.', file=sys.stderr)
        return 1

    convert_file(input_path, output_path, title=args.title)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
