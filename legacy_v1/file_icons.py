"""
AI Fervv IDE - Enhanced File Icons
Comprehensive file type icons and detection
"""

FILE_ICONS = {
    # Programming Languages
    ".py": "🐍",
    ".js": "📜",
    ".ts": "📘",
    ".jsx": "⚛️",
    ".tsx": "⚛️",
    ".java": "☕",
    ".cpp": "🔷",
    ".c": "🔵",
    ".cs": "🎯",
    ".go": "🐹",
    ".rs": "🦀",
    ".php": "🐘",
    ".rb": "💎",
    ".swift": "🕊️",
    ".kt": "🎨",
    
    # Web
    ".html": "🌐",
    ".htm": "🌐",
    ".css": "🎨",
    ".scss": "🎨",
    ".sass": "🎨",
    ".less": "🎨",
    
    # Data & Config
    ".json": "{}",
    ".xml": "📋",
    ".yaml": "⚙️",
    ".yml": "⚙️",
    ".toml": "⚙️",
    ".ini": "⚙️",
    ".conf": "⚙️",
    ".config": "⚙️",
    
    # Documentation
    ".md": "📝",
    ".txt": "📄",
    ".pdf": "📕",
    ".doc": "📘",
    ".docx": "📘",
    
    # Images
    ".png": "🖼️",
    ".jpg": "🖼️",
    ".jpeg": "🖼️",
    ".gif": "🖼️",
    ".svg": "🎨",
    ".ico": "🎯",
    ".webp": "🖼️",
    
    # Archives
    ".zip": "📦",
    ".rar": "📦",
    ".7z": "📦",
    ".tar": "📦",
    ".gz": "📦",
    
    # Executables
    ".exe": "🚀",
    ".app": "🚀",
    ".bat": "⚙️",
    ".sh": "⚙️",
    ".ps1": "💻",
    
    # Database
    ".db": "🗄️",
    ".sqlite": "🗄️",
    ".sql": "🗄️",
    
    # Other
    ".gitignore": "🔧",
    ".env": "🔒",
    ".lock": "🔒",
    "folder": "📁",
    "folder_open": "📂",
    "default": "📄"
}

# Special file names
SPECIAL_FILES = {
    "README.md": "📖",
    "LICENSE": "⚖️",
    "package.json": "📦",
    "requirements.txt": "📋",
    "Dockerfile": "🐳",
    "docker-compose.yml": "🐳",
    ".gitignore": "🔧",
    ".env": "🔒",
    "Makefile": "🔨",
    ".travis.yml": "🔄",
    ".gitlab-ci.yml": "🔄"
}

def get_file_icon(filename, is_directory=False):
    """Get icon for file based on name or extension"""
    if is_directory:
        return FILE_ICONS["folder"]
    
    # Check special files first
    if filename in SPECIAL_FILES:
        return SPECIAL_FILES[filename]
    
    # Check extension
    import os
    ext = os.path.splitext(filename)[1].lower()
    
    return FILE_ICONS.get(ext, FILE_ICONS["default"])

def get_language_from_extension(filename):
    """Detect programming language from file extension"""
    import os
    ext = os.path.splitext(filename)[1].lower()
    
    language_map = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".jsx": "javascript",
        ".tsx": "typescript",
        ".html": "html",
        ".htm": "html",
        ".css": "css",
        ".scss": "css",
        ".sass": "css",
        ".json": "json",
        ".xml": "xml",
        ".java": "java",
        ".cpp": "cpp",
        ".c": "c",
        ".cs": "csharp",
        ".php": "php",
        ".rb": "ruby",
        ".go": "go",
        ".rs": "rust",
        ".swift": "swift",
        ".kt": "kotlin",
        ".md": "markdown",
        ".sh": "bash",
        ".bat": "batch",
        ".ps1": "powershell",
        ".sql": "sql"
    }
    
    return language_map.get(ext, "text")
