"""
Polyglot Language Registry
Defines syntax highlighting rules and language metadata.
"""
import re

class LanguageRegistry:
    def __init__(self):
        self.languages = {}
        self._init_defaults()

    def _init_defaults(self):
        # Python
        self.register("python", {
            "keywords": ["def", "class", "import", "from", "return", "if", "else", "elif", "while", "for", "in", "try", "except", "with", "as", "async", "await", "lambda"],
            "builtins": ["print", "len", "range", "str", "int", "float", "list", "dict", "set", "super", "__init__"],
            "comments": r"#.*",
            "strings": r"(\"(\\\"|[^\"])*\")|('(\\\'|[^'])*')",
            "decorators": r"@\w+"
        })
        
        # JavaScript / TypeScript
        self.register("javascript", {
            "keywords": ["function", "const", "let", "var", "return", "if", "else", "for", "while", "class", "import", "export", "default", "async", "await", "new", "this", "try", "catch"],
            "builtins": ["console", "log", "document", "window", "setTimeout", "setInterval", "Promise", "JSON"],
            "comments": r"//.*",
            "strings": r"(\"(\\\"|[^\"])*\")|('(\\\'|[^'])*')|(`([^`])*`)", # Backticks for template strings
            "decorators": r"@\w+"
        })
        
        # HTML
        self.register("html", {
            "keywords": ["html", "head", "body", "div", "span", "p", "a", "img", "script", "style", "link", "meta", "h1", "h2", "h3", "ul", "li", "table", "tr", "td", "button", "input", "form"],
            "builtins": ["src", "href", "class", "id", "style", "type", "onclick", "name", "value", "placeholder"],
            "comments": r"<!--.*?-->",
            "strings": r"(\"(\\\"|[^\"])*\")|('(\\\'|[^'])*')"
        })
        
        # C++
        self.register("cpp", {
            "keywords": ["int", "float", "double", "char", "void", "return", "if", "else", "while", "for", "class", "struct", "public", "private", "protected", "virtual", "override", "new", "delete", "using", "namespace", "include", "template", "typename"],
            "builtins": ["std", "cout", "cin", "endl", "vector", "string", "map", "size_t", "printf"],
            "comments": r"(//.*)|(/\*.*?\*/)", 
            "strings": r"(\"(\\\"|[^\"])*\")|('(\\\'|[^'])*')",
            "decorators": r"#\w+" # Preprocessor
        })

        # TypeScript / TSX
        self.register("typescript", {
            "keywords": ["interface", "type", "enum", "namespace", "declare", "module", "as", "is", "keyof", "readonly", "implements", "function", "const", "let", "var", "return", "if", "else", "for", "while", "class", "import", "export", "default", "async", "await", "new", "this", "try", "catch"],
            "builtins": ["console", "log", "document", "window", "Promise", "JSON", "any", "string", "number", "boolean", "void", "never", "unknown"],
            "comments": r"(//.*)|(/\*.*?\*/)",
            "strings": r"(\"(\\\"|[^\"])*\")|('(\\\'|[^'])*')|(`([^`])*`)",
            "decorators": r"@\w+"
        })

    def register(self, name, rules):
        self.languages[name] = rules

    def detect_language(self, filename):
        ext = filename.split('.')[-1].lower()
        mapping = {
            "py": "python", "pyw": "python",
            "js": "javascript", "jsx": "javascript",
            "ts": "typescript", "tsx": "typescript",
            "html": "html", "htm": "html",
            "css": "css",
            "cpp": "cpp", "c": "cpp", "h": "cpp", "hpp": "cpp",
            "rs": "rust",
            "md": "markdown",
            "json": "json"
        }
        return mapping.get(ext, "python")

    def get_rules(self, language):
        return self.languages.get(language, self.languages["python"])

language_registry = LanguageRegistry()
