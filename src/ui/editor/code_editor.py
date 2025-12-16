"""
Code Editor Component
Enhanced text editor with Gutter, Line Numbers, and Syntax Highlighting.
"""
import customtkinter as ctk
from src.ui.editor.syntax_highlighter import SyntaxHighlighter
from src.core.container import get_service

class CodeEditor(ctk.CTkFrame):
    def __init__(self, master, file_ext="py", file_path=None, **kwargs):
        super().__init__(master, **kwargs)
        self.theme = get_service("ThemeService")
        self.file_service = get_service("FileService")
        self.file_ext = file_ext
        self.file_path = file_path
        
        # Debounce State
        self._highlight_timer = None
        
        # Configuration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # 1. Line Numbers (Gutter)
        self.line_numbers = ctk.CTkTextbox(
            self, width=40, font=("Consolas", 14),
            fg_color=self.theme.get_color("line_num_bg"),
            text_color=self.theme.get_color("line_num_fg"),
            activate_scrollbars=False
        )
        self.line_numbers.grid(row=0, column=0, sticky="ns")
        self.line_numbers.insert("1.0", "1")
        self.line_numbers.configure(state="disabled")
        
        # 2. Main Text Area
        self.textbox = ctk.CTkTextbox(
            self, wrap="none", font=("Consolas", 14),
            undo=True,
            fg_color=self.theme.get_color("bg_main"),
            text_color=self.theme.get_color("fg_text")
        )
        self.textbox.grid(row=0, column=1, sticky="nsew")
        
        # 3. Syntax Highlighting
        self.highlighter = SyntaxHighlighter(self.textbox, self.file_ext)
        
        # 4. Load Content if path provided
        if self.file_path:
            content = self.file_service.read_file(self.file_path)
            if content:
                self.textbox.insert("1.0", content)
                self.highlighter.highlight()
                self.update_line_numbers()

        # Bindings
        self.textbox.bind("<KeyRelease>", self.on_key_release)
        self.textbox.bind("<MouseWheel>", self.sync_scroll)
        self.line_numbers.bind("<MouseWheel>", self.sync_scroll)
        
        # Ctrl+S to save
        self.textbox.bind("<Control-s>", self.save_file)

    def save_file(self, event=None):
        if self.file_path:
            content = self.textbox.get("1.0", "end-1c")
            if self.file_service.write_file(self.file_path, content):
                print(f"Saved {self.file_path}")
        else:
            print("No file path set. Save As not implemented.")

    def on_key_release(self, event):
        self.update_line_numbers()
        self.debounce_highlight()

    def debounce_highlight(self):
        if self._highlight_timer:
            self.after_cancel(self._highlight_timer)
        self._highlight_timer = self.after(300, self.highlighter.highlight)

    def update_line_numbers(self):
        lines = self.textbox.get("1.0", "end-1c").split("\n")
        line_count = len(lines)
        new_nums = "\n".join(str(i) for i in range(1, line_count + 1))
        
        self.line_numbers.configure(state="normal")
        self.line_numbers.delete("1.0", "end")
        self.line_numbers.insert("1.0", new_nums)
        self.line_numbers.configure(state="disabled")

    def sync_scroll(self, event):
        # Sync Y-scroll
        self.line_numbers.yview_moveto(self.textbox.yview()[0])
