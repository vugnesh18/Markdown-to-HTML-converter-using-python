"""Markdown to HTML converter with a graphical user interface."""

import pathlib
import tempfile
import webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from converter import build_html_document, convert_markdown_to_html


class MarkdownToHtmlApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title('Markdown to HTML Converter')
        self.geometry('1100x700')
        self.minsize(900, 600)

        self._create_style()
        self._create_widgets()
        self._create_layout()

    def _create_style(self) -> None:
        style = ttk.Style(self)
        style.configure('TButton', padding=8)
        style.configure('TLabel', padding=4)
        style.configure('Header.TLabel', font=('Segoe UI', 18, 'bold'))
        style.configure('Section.TLabel', font=('Segoe UI', 12, 'bold'))

    def _create_widgets(self) -> None:
        self.header = ttk.Label(self, text='Markdown to HTML Converter', style='Header.TLabel')
        self.description = ttk.Label(self, text='Load Markdown, preview HTML source, and save a polished HTML file.', wraplength=840)

        self.open_button = ttk.Button(self, text='Open Markdown', command=self.open_markdown)
        self.convert_button = ttk.Button(self, text='Convert', command=self.convert_markdown)
        self.preview_button = ttk.Button(self, text='Preview in Browser', command=self.preview_html)
        self.save_button = ttk.Button(self, text='Save HTML', command=self.save_html)
        self.clear_button = ttk.Button(self, text='Clear', command=self.clear_all)

        self.markdown_label = ttk.Label(self, text='Markdown Input', style='Section.TLabel')
        self.html_label = ttk.Label(self, text='HTML Output', style='Section.TLabel')

        self.input_text = tk.Text(self, wrap='word', font=('Consolas', 11), undo=True)
        self.output_text = tk.Text(self, wrap='word', font=('Consolas', 11), state='disabled', bg='#f3f4f6')

        self.status = ttk.Label(self, text='Ready', anchor='w')

    def _create_layout(self) -> None:
        button_frame = ttk.Frame(self)
        button_frame.grid(row=2, column=0, columnspan=2, sticky='ew', padx=12, pady=(0, 8))
        button_frame.columnconfigure((0, 1, 2, 3, 4), weight=1)

        self.header.grid(row=0, column=0, columnspan=2, sticky='w', padx=12, pady=(12, 2))
        self.description.grid(row=1, column=0, columnspan=2, sticky='w', padx=12)

        button_frame.grid(row=2, column=0, columnspan=2, sticky='ew', padx=12, pady=(10, 10))
        self.open_button.grid(row=0, column=0, padx=4, sticky='ew')
        self.convert_button.grid(row=0, column=1, padx=4, sticky='ew')
        self.preview_button.grid(row=0, column=2, padx=4, sticky='ew')
        self.save_button.grid(row=0, column=3, padx=4, sticky='ew')
        self.clear_button.grid(row=0, column=4, padx=4, sticky='ew')

        self.markdown_label.grid(row=3, column=0, sticky='w', padx=12)
        self.html_label.grid(row=3, column=1, sticky='w', padx=12)

        self.input_text.grid(row=4, column=0, sticky='nsew', padx=(12, 6), pady=(0, 12))
        self.output_text.grid(row=4, column=1, sticky='nsew', padx=(6, 12), pady=(0, 12))

        self.status.grid(row=5, column=0, columnspan=2, sticky='ew', padx=12, pady=(0, 12))

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(4, weight=1)

    def open_markdown(self) -> None:
        path = filedialog.askopenfilename(
            title='Open Markdown File',
            filetypes=[('Markdown files', '*.md;*.markdown'), ('Text files', '*.txt'), ('All files', '*.*')],
        )
        if not path:
            return

        try:
            content = pathlib.Path(path).read_text(encoding='utf-8')
            self.input_text.delete('1.0', 'end')
            self.input_text.insert('1.0', content)
            self.set_status(f'Loaded {path}')
        except OSError as error:
            messagebox.showerror('Open Error', f'Could not open file: {error}')
            self.set_status('Failed to load file')

    def convert_markdown(self) -> None:
        markdown = self.input_text.get('1.0', 'end').strip()
        if not markdown:
            messagebox.showwarning('Empty Markdown', 'Please enter Markdown text before converting.')
            return

        body_html = convert_markdown_to_html(markdown)
        html_document = build_html_document(body_html, title='Markdown Conversion')

        self.output_text.configure(state='normal')
        self.output_text.delete('1.0', 'end')
        self.output_text.insert('1.0', html_document)
        self.output_text.configure(state='disabled')
        self.set_status('Converted Markdown to HTML')

    def preview_html(self) -> None:
        html_text = self.get_output_html()
        if not html_text:
            messagebox.showwarning('No HTML Available', 'Convert Markdown first before previewing.')
            return

        with tempfile.NamedTemporaryFile('w', suffix='.html', delete=False, encoding='utf-8') as temp_file:
            temp_file.write(html_text)
            preview_path = pathlib.Path(temp_file.name)

        webbrowser.open_new_tab(preview_path.as_uri())
        self.set_status(f'Preview opened in browser: {preview_path.name}')

    def save_html(self) -> None:
        html_text = self.get_output_html()
        if not html_text:
            messagebox.showwarning('No HTML Available', 'Convert Markdown first before saving.')
            return

        path = filedialog.asksaveasfilename(
            title='Save HTML File',
            defaultextension='.html',
            filetypes=[('HTML files', '*.html'), ('All files', '*.*')],
        )
        if not path:
            return

        try:
            pathlib.Path(path).write_text(html_text, encoding='utf-8')
            self.set_status(f'Saved HTML file: {path}')
            messagebox.showinfo('Saved', f'HTML saved to {path}')
        except OSError as error:
            messagebox.showerror('Save Error', f'Could not save file: {error}')
            self.set_status('Failed to save HTML file')

    def clear_all(self) -> None:
        self.input_text.delete('1.0', 'end')
        self.output_text.configure(state='normal')
        self.output_text.delete('1.0', 'end')
        self.output_text.configure(state='disabled')
        self.set_status('Cleared editor content')

    def get_output_html(self) -> str:
        return self.output_text.get('1.0', 'end').strip()

    def set_status(self, message: str) -> None:
        self.status.configure(text=message)


if __name__ == '__main__':
    app = MarkdownToHtmlApp()
    app.mainloop()
