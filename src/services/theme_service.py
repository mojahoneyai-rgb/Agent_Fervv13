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
        self.set_theme("VS Code Dark+")
        
    def _register_default_themes(self):
        self.register_theme(Theme("VS Code Dark+", {
            "bg_main": "#1e1e1e", "bg_sidebar": "#252526", "bg_activity": "#333333",
            "bg_status": "#007acc", "fg_text": "#d4d4d4", "fg_comment": "#6a9955",
            "fg_keyword": "#569cd6", "fg_string": "#ce9178", "fg_function": "#dcdcaa",
            "fg_number": "#b5cea8", "border": "#474747", "hover": "#3e3e42",
            "select": "#37373d", "line_num_bg": "#1e1e1e", "line_num_fg": "#858585",
            "error": "#f48771", "warning": "#cca700", "success": "#89d185"
        }))
        # Add more themes here (Solarized, Cyberpunk, etc.) as implemented previously
        # For brevity in this initial file, we start with one. 
        # The full list will be migrated.

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
