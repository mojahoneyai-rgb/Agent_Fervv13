"""
AI Fervv IDE - Autocomplete System
Intelligent code completion and suggestions
"""

import re

class AutocompleteEngine:
    def __init__(self):
        self.keywords = {
            "python": [
                "def", "class", "import", "from", "return", "if", "else", "elif",
                "while", "for", "in", "try", "except", "finally", "with", "as",
                "True", "False", "None", "and", "or", "not", "is", "lambda",
                "pass", "break", "continue", "global", "nonlocal", "assert",
                "del", "raise", "yield", "async", "await"
            ],
            "javascript": [
                "function", "const", "let", "var", "if", "else", "for", "while",
                "switch", "case", "break", "continue", "return", "try", "catch",
                "finally", "throw", "async", "await", "class", "extends", "import",
                "export", "default", "new", "this", "super", "static"
            ],
            "html": [
                "div", "span", "p", "a", "img", "ul", "li", "ol", "table", "tr",
                "td", "th", "form", "input", "button", "select", "option", "textarea",
                "h1", "h2", "h3", "h4", "h5", "h6", "header", "footer", "nav",
                "section", "article", "aside", "main"
            ],
            "css": [
                "color", "background", "margin", "padding", "border", "width", "height",
                "display", "position", "top", "left", "right", "bottom", "flex",
                "grid", "font-size", "font-family", "font-weight", "text-align",
                "justify-content", "align-items", "transform", "transition", "animation"
            ]
        }
        
        self.common_modules = {
            "python": [
                "os", "sys", "json", "re", "time", "datetime", "random", "math",
                "collections", "itertools", "functools", "pathlib", "typing",
                "subprocess", "threading", "multiprocessing", "requests", "flask",
                "django", "numpy", "pandas", "matplotlib", "tkinter", "customtkinter"
            ]
        }
        
        self.user_symbols = {}  # Track user-defined functions, classes, variables
    
    def get_suggestions(self, text, cursor_pos, language="python"):
        """Get autocomplete suggestions based on current text and cursor position"""
        # Get word being typed
        current_word = self._get_current_word(text, cursor_pos)
        
        if not current_word:
            return []
        
        suggestions = []
        
        # 1. Language keywords
        lang = language.lower()
        if lang in self.keywords:
            for keyword in self.keywords[lang]:
                if keyword.startswith(current_word):
                    suggestions.append({
                        "text": keyword,
                        "type": "keyword",
                        "icon": "🔑"
                    })
        
        # 2. Common modules (for imports)
        if lang in self.common_modules and ("import" in text or "from" in text):
            for module in self.common_modules[lang]:
                if module.startswith(current_word):
                    suggestions.append({
                        "text": module,
                        "type": "module",
                        "icon": "📦"
                    })
        
        # 3. User-defined symbols
        if lang in self.user_symbols:
            for symbol, symbol_type in self.user_symbols[lang].items():
                if symbol.startswith(current_word):
                    icon = "📘" if symbol_type == "class" else "⚡"
                    suggestions.append({
                        "text": symbol,
                        "type": symbol_type,
                        "icon": icon
                    })
        
        # 4. HTML tag autocomplete
        if lang == "html" and current_word.startswith("<"):
            word = current_word[1:]
            for tag in self.keywords["html"]:
                if tag.startswith(word):
                    suggestions.append({
                        "text": f"<{tag}></{tag}>",
                        "type": "tag",
                        "icon": "🏷️"
                    })
        
        return suggestions[:10]  # Limit to 10 suggestions
    
    def _get_current_word(self, text, cursor_pos):
        """Extract the word being typed at cursor position"""
        if cursor_pos == 0:
            return ""
        
        # Find word boundaries
        start = cursor_pos
        while start > 0 and text[start - 1].isalnum() or (start > 0 and text[start - 1] in "_.<"):
            start -= 1
        
        return text[start:cursor_pos]
    
    def analyze_code(self, code, language="python"):
        """Analyze code to extract user-defined symbols"""
        lang = language.lower()
        
        if lang not in self.user_symbols:
            self.user_symbols[lang] = {}
        
        if lang == "python":
            # Find function definitions
            func_pattern = r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\("
            for match in re.finditer(func_pattern, code):
                self.user_symbols[lang][match.group(1)] = "function"
            
            # Find class definitions
            class_pattern = r"class\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*[:\(]"
            for match in re.finditer(class_pattern, code):
                self.user_symbols[lang][match.group(1)] = "class"
        
        elif lang == "javascript":
            # Find function definitions
            func_pattern = r"function\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\("
            for match in re.finditer(func_pattern, code):
                self.user_symbols[lang][match.group(1)] = "function"
            
            # Find const/let/var declarations
            var_pattern = r"(?:const|let|var)\s+([a-zA-Z_][a-zA-Z0-9_]*)"
            for match in re.finditer(var_pattern, code):
                self.user_symbols[lang][match.group(1)] = "variable"
            
            # Find class definitions
            class_pattern = r"class\s+([a-zA-Z_][a-zA-Z0-9_]*)"
            for match in re.finditer(class_pattern, code):
                self.user_symbols[lang][match.group(1)] = "class"
    
    def get_snippet_completion(self, trigger, language="python"):
        """Get snippet completion for triggers like 'if', 'for', etc."""
        snippets = {
            "python": {
                "if": "if condition:\n    pass",
                "for": "for item in iterable:\n    pass",
                "while": "while condition:\n    pass",
                "def": "def function_name():\n    pass",
                "class": "class ClassName:\n    def __init__(self):\n        pass"
            },
            "javascript": {
                "if": "if (condition) {\n    \n}",
                "for": "for (let i = 0; i < array.length; i++) {\n    \n}",
                "function": "function functionName() {\n    \n}",
                "class": "class ClassName {\n    constructor() {\n        \n    }\n}"
            }
        }
        
        lang = language.lower()
        if lang in snippets and trigger in snippets[lang]:
            return snippets[lang][trigger]
        
        return None
