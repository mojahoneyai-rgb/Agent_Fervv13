"""
AI Fervv IDE - Theme System
Advanced theme management with multiple predefined color schemes
"""

class Theme:
    def __init__(self, name, colors):
        self.name = name
        self.colors = colors

# Predefined themes
THEMES = {
    "VS Code Dark+": Theme("VS Code Dark+", {
        "bg_main": "#1e1e1e",
        "bg_sidebar": "#252526",
        "bg_activity": "#333333",
        "bg_status": "#007acc",
        "fg_text": "#d4d4d4",
        "fg_comment": "#6a9955",
        "fg_keyword": "#569cd6",
        "fg_string": "#ce9178",
        "fg_function": "#dcdcaa",
        "fg_number": "#b5cea8",
        "border": "#3c3c3c",
        "hover": "#2a2d2e",
        "select": "#094771",
        "line_num_bg": "#1e1e1e",
        "line_num_fg": "#858585",
        "error": "#f48771",
        "warning": "#cca700",
        "success": "#89d185"
    }),
    
    "Dracula": Theme("Dracula", {
        "bg_main": "#282a36",
        "bg_sidebar": "#21222c",
        "bg_activity": "#191a21",
        "bg_status": "#bd93f9",
        "fg_text": "#f8f8f2",
        "fg_comment": "#6272a4",
        "fg_keyword": "#ff79c6",
        "fg_string": "#f1fa8c",
        "fg_function": "#50fa7b",
        "fg_number": "#bd93f9",
        "border": "#44475a",
        "hover": "#44475a",
        "select": "#44475a",
        "line_num_bg": "#282a36",
        "line_num_fg": "#6272a4",
        "error": "#ff5555",
        "warning": "#ffb86c",
        "success": "#50fa7b"
    }),
    
    "Monokai": Theme("Monokai", {
        "bg_main": "#272822",
        "bg_sidebar": "#1e1f1c",
        "bg_activity": "#2e2e2e",
        "bg_status": "#75715e",
        "fg_text": "#f8f8f2",
        "fg_comment": "#75715e",
        "fg_keyword": "#f92672",
        "fg_string": "#e6db74",
        "fg_function": "#a6e22e",
        "fg_number": "#ae81ff",
        "border": "#3e3d32",
        "hover": "#3e3d32",
        "select": "#49483e",
        "line_num_bg": "#272822",
        "line_num_fg": "#90908a",
        "error": "#f92672",
        "warning": "#fd971f",
        "success": "#a6e22e"
    }),
    
    "Nord": Theme("Nord", {
        "bg_main": "#2e3440",
        "bg_sidebar": "#3b4252",
        "bg_activity": "#434c5e",
        "bg_status": "#5e81ac",
        "fg_text": "#eceff4",
        "fg_comment": "#616e88",
        "fg_keyword": "#81a1c1",
        "fg_string": "#a3be8c",
        "fg_function": "#88c0d0",
        "fg_number": "#b48ead",
        "border": "#4c566a",
        "hover": "#434c5e",
        "select": "#434c5e",
        "line_num_bg": "#2e3440",
        "line_num_fg": "#4c566a",
        "error": "#bf616a",
        "warning": "#ebcb8b",
        "success": "#a3be8c"
    }),
    
    "GitHub Light": Theme("GitHub Light", {
        "bg_main": "#ffffff",
        "bg_sidebar": "#f6f8fa",
        "bg_activity": "#e1e4e8",
        "bg_status": "#0366d6",
        "fg_text": "#24292e",
        "fg_comment": "#6a737d",
        "fg_keyword": "#d73a49",
        "fg_string": "#032f62",
        "fg_function": "#6f42c1",
        "fg_number": "#005cc5",
        "border": "#e1e4e8",
        "hover": "#f6f8fa",
        "select": "#c8e1ff",
        "line_num_bg": "#ffffff",
        "line_num_fg": "#959da5",
        "error": "#d73a49",
        "warning": "#e36209",
        "success": "#28a745"
    }),
    
    "Oceanic": Theme("Oceanic", {
        "bg_main": "#1b2b34",
        "bg_sidebar": "#343d46",
        "bg_activity": "#4f5b66",
        "bg_status": "#6699cc",
        "fg_text": "#c0c5ce",
        "fg_comment": "#65737e",
        "fg_keyword": "#c594c5",
        "fg_string": "#99c794",
        "fg_function": "#6699cc",
        "fg_number": "#f99157",
        "border": "#343d46",
        "hover": "#343d46",
        "select": "#4f5b66",
        "line_num_bg": "#1b2b34",
        "line_num_fg": "#65737e",
        "error": "#ec5f67",
        "warning": "#fac863",
        "success": "#99c794"
    }),

    "Solarized Dark": Theme("Solarized Dark", {
        "bg_main": "#002b36",
        "bg_sidebar": "#073642",
        "bg_activity": "#002b36",
        "bg_status": "#2aa198",
        "fg_text": "#839496",
        "fg_comment": "#586e75",
        "fg_keyword": "#859900",
        "fg_string": "#2aa198",
        "fg_function": "#268bd2",
        "fg_number": "#d33682",
        "border": "#073642",
        "hover": "#073642",
        "select": "#073642",
        "line_num_bg": "#002b36",
        "line_num_fg": "#586e75",
        "error": "#dc322f",
        "warning": "#b58900",
        "success": "#859900"
    }),

    "Night Owl": Theme("Night Owl", {
        "bg_main": "#011627",
        "bg_sidebar": "#011627",
        "bg_activity": "#011627",
        "bg_status": "#7e57c2",
        "fg_text": "#d6deeb",
        "fg_comment": "#637777",
        "fg_keyword": "#c792ea",
        "fg_string": "#ecc48d",
        "fg_function": "#82aaff",
        "fg_number": "#f78c6c",
        "border": "#5f7e97",
        "hover": "#1d3b53",
        "select": "#1d3b53",
        "line_num_bg": "#011627",
        "line_num_fg": "#7fdbca",
        "error": "#ef5350",
        "warning": "#addb67",
        "success": "#22da6e"
    }),

    "Cyberpunk": Theme("Cyberpunk", {
        "bg_main": "#0d0221",
        "bg_sidebar": "#1a0440",
        "bg_activity": "#2a0467",
        "bg_status": "#ff0099",
        "fg_text": "#00ff99",
        "fg_comment": "#674ab3",
        "fg_keyword": "#ff0099",
        "fg_string": "#f3e108",
        "fg_function": "#00d7ff",
        "fg_number": "#ff6d00",
        "border": "#ff0099",
        "hover": "#37155a",
        "select": "#3b0870",
        "line_num_bg": "#0d0221",
        "line_num_fg": "#00ff99",
        "error": "#ff003c",
        "warning": "#f3e108",
        "success": "#00ff99"
    }),

    "SynthWave '84": Theme("SynthWave '84", {
        "bg_main": "#262335",
        "bg_sidebar": "#241b2f",
        "bg_activity": "#262335",
        "bg_status": "#34294f",
        "fg_text": "#b6b1b1",
        "fg_comment": "#848bbd",
        "fg_keyword": "#f45f93",
        "fg_string": "#ff7170",
        "fg_function": "#36f9f6",
        "fg_number": "#f9c859",
        "border": "#495495",
        "hover": "#34294f",
        "select": "#34294f",
        "line_num_bg": "#262335",
        "line_num_fg": "#495495",
        "error": "#f92672",
        "warning": "#f9c859",
        "success": "#36f9f6"
    }),

    "Material Ocean": Theme("Material Ocean", {
        "bg_main": "#0f111a",
        "bg_sidebar": "#090b10",
        "bg_activity": "#0f111a",
        "bg_status": "#009688",
        "fg_text": "#a6accd",
        "fg_comment": "#464b5d",
        "fg_keyword": "#c792ea",
        "fg_string": "#c3e88d",
        "fg_function": "#82aaff",
        "fg_number": "#f78c6c",
        "border": "#292d3e",
        "hover": "#1f2233",
        "select": "#292d3e",
        "line_num_bg": "#0f111a",
        "line_num_fg": "#3b3f51",
        "error": "#ff5370",
        "warning": "#ffcb6b",
        "success": "#c3e88d"
    }),
    
    "Deep Blue": Theme("Deep Blue", {
         "bg_main": "#000b1e",
         "bg_sidebar": "#001233",
         "bg_activity": "#001a4d",
         "bg_status": "#004085",
         "fg_text": "#cce5ff",
         "fg_comment": "#5c8a8a",
         "fg_keyword": "#3399ff",
         "fg_string": "#99ccff",
         "fg_function": "#66b3ff",
         "fg_number": "#99e6ff",
         "border": "#00264d",
         "hover": "#00264d",
         "select": "#004085",
         "line_num_bg": "#000b1e",
         "line_num_fg": "#003366",
         "error": "#ff3333",
         "warning": "#ffcc00",
         "success": "#33cc33"
    })
}

class ThemeManager:
    def __init__(self):
        self.current_theme = "VS Code Dark+"
        self.custom_themes = {}
    
    def get_current_theme(self):
        """Get current active theme"""
        if self.current_theme in THEMES:
            return THEMES[self.current_theme]
        elif self.current_theme in self.custom_themes:
            return self.custom_themes[self.current_theme]
        return THEMES["VS Code Dark+"]  # Fallback
    
    def get_color(self, key):
        """Get specific color from current theme"""
        theme = self.get_current_theme()
        return theme.colors.get(key, "#ffffff")
    
    def set_theme(self, theme_name):
        """Switch to different theme"""
        if theme_name in THEMES or theme_name in self.custom_themes:
            self.current_theme = theme_name
            return True
        return False
    
    def get_all_themes(self):
        """Get list of all available themes"""
        return list(THEMES.keys()) + list(self.custom_themes.keys())
    
    def create_custom_theme(self, name, colors):
        """Create a custom theme"""
        self.custom_themes[name] = Theme(name, colors)
        return True
    
    def export_theme(self, theme_name):
        """Export theme to dict for saving"""
        theme = None
        if theme_name in THEMES:
            theme = THEMES[theme_name]
        elif theme_name in self.custom_themes:
            theme = self.custom_themes[theme_name]
        
        if theme:
            return {"name": theme.name, "colors": theme.colors}
        return None
    
    def import_theme(self, theme_data):
        """Import theme from dict"""
        if "name" in theme_data and "colors" in theme_data:
            self.create_custom_theme(theme_data["name"], theme_data["colors"])
            return True
        return False
