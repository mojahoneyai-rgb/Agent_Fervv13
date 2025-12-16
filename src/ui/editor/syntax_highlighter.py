"""
Syntax Highlighter
Applies text tags based on LanguageRegistry rules.
"""
import tkinter as tk
from src.languages.language_registry import language_registry
from src.core.container import get_service
import re
import threading

class SyntaxHighlighter:
    def __init__(self, text_widget, file_ext):
        self.text_widget = text_widget
        self.language = language_registry.detect_language(f"dummy.{file_ext}")
        self.rules = language_registry.get_rules(self.language)
        self.theme = get_service("ThemeService")
        
        self.setup_tags()

    def setup_tags(self):
        # Define tag colors based on theme
        colors = self.theme._current_theme.colors if self.theme._current_theme else {}
        
        self.text_widget.tag_config("keyword", foreground=colors.get("fg_keyword", "#569cd6"))
        self.text_widget.tag_config("string", foreground=colors.get("fg_string", "#ce9178"))
        self.text_widget.tag_config("comment", foreground=colors.get("fg_comment", "#6a9955"))
        self.text_widget.tag_config("decorator", foreground=colors.get("fg_function", "#dcdcaa"))
        self.text_widget.tag_config("builtin", foreground=colors.get("fg_function", "#dcdcaa"))

    def highlight(self):
        # Run highlighting
        content = self.text_widget.get("1.0", "end-1c")
        self.clear_tags()
        
        # Apply Regex Rules
        self._apply_regex(self.rules.get("comments"), "comment", content)
        self._apply_regex(self.rules.get("strings"), "string", content)
        
        for kw in self.rules.get("keywords", []):
            self._apply_word_match(kw, "keyword", content)
            
        for bi in self.rules.get("builtins", []):
            self._apply_word_match(bi, "builtin", content)

    def _apply_regex(self, pattern, tag, content):
        if not pattern: return
        try:
            for match in re.finditer(pattern, content, re.MULTILINE):
                start = f"1.0 + {match.start()} chars"
                end = f"1.0 + {match.end()} chars"
                self.text_widget.tag_add(tag, start, end)
        except:
            pass

    def _apply_word_match(self, word, tag, content):
        start_idx = "1.0"
        while True:
            pos = self.text_widget.search(word, start_idx, stopindex="end", regex=False)
            if not pos: break
            
            # Check formatting
            end_pos = f"{pos}+{len(word)}c"
            
            # TODO: Add word boundary check
            self.text_widget.tag_add(tag, pos, end_pos)
            start_idx = end_pos

    def clear_tags(self):
        for tag in ["keyword", "string", "comment", "decorator", "builtin"]:
            self.text_widget.tag_remove(tag, "1.0", "end")
