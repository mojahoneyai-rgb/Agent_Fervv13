"""
Theme Service
Manages application themes and color palettes.
"""
from src.core.event_bus import global_event_bus
from src.core.container import get_service

class Theme:
    def __init__(self, name, colors):
        self.name = name
        self.colors = colors

class ThemeService:
    def __init__(self):
        self._themes = {}
        self._current_theme = None
        
        # Load Defaults
        self._register_default_themes()
        self.set_theme("Cyberpunk Neon")
        
    def _register_default_themes(self):
        self.register_theme(Theme("VS Code Dark+", {
            "bg_main": "#1e1e1e", "bg_sidebar": "#252526", "bg_activity": "#333333",
            "bg_status": "#007acc", "fg_text": "#d4d4d4", "fg_comment": "#6a9955",
            "fg_keyword": "#569cd6", "fg_string": "#ce9178", "fg_function": "#dcdcaa",
            "fg_number": "#b5cea8", "border": "#474747", "hover": "#3e3e42",
            "select": "#37373d", "line_num_bg": "#1e1e1e", "line_num_fg": "#858585",
            "error": "#f48771", "warning": "#cca700", "success": "#89d185"
        }))
        
        self.register_theme(Theme("Cyberpunk Neon", {
            "bg_main": "#1e1e2e",       # Lighter dark blue-gray (like VS Code)
            "bg_sidebar": "#252535",    # Slightly lighter sidebar
            "bg_activity": "#1a1a28",   # Activity bar darker
            "bg_status": "#007acc",     # Blue status bar (VS Code style)
            "fg_text": "#d4d4d4", 
            "fg_comment": "#6a9955",
            "fg_keyword": "#c678dd",    # Purple keywords
            "fg_string": "#98c379",     # Green strings
            "fg_function": "#61afef",   # Blue functions
            "fg_number": "#d19a66", 
            "border": "#3d3d5c", 
            "hover": "#2a2a40",
            "select": "#3d3d5c", 
            "line_num_bg": "#1e1e2e", 
            "line_num_fg": "#858585",
            "error": "#f44747", 
            "warning": "#cca700", 
            "success": "#89d185"
        }))

        self.register_theme(Theme("Modern Light", {
            "bg_main": "#ffffff", "bg_sidebar": "#f3f3f3", "bg_activity": "#e8e8e8",
            "bg_status": "#007acc", "fg_text": "#333333", "fg_comment": "#008000",
            "fg_keyword": "#0000ff", "fg_string": "#a31515", "fg_function": "#795e26",
            "fg_number": "#098658", "border": "#e5e5e5", "hover": "#e8e8e8",
            "select": "#add6ff", "line_num_bg": "#ffffff", "line_num_fg": "#2b91af",
            "error": "#cd3131", "warning": "#cca700", "success": "#098658"
        }))

        self.set_theme("Cyberpunk Neon")

    def register_theme(self, theme: Theme):
        self._themes[theme.name] = theme

    def set_theme(self, theme_name):
        if theme_name in self._themes:
            self._current_theme = self._themes[theme_name]
            config = get_service("ConfigService")
            if config:
                config.set("theme", theme_name)
            global_event_bus.publish("theme_changed", self._current_theme)

    def get_color(self, key):
        if self._current_theme:
            return self._current_theme.colors.get(key, "#000000")
        return "#000000"

    def get_all_themes(self):
        return list(self._themes.keys())
