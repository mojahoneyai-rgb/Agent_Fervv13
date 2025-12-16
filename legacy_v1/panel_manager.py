"""
AI Fervv IDE - Panel Manager
Resizable panel management system
"""

class PanelManager:
    """Manages resizable panels and layouts"""
    
    def __init__(self):
        self.panels = {}
        self.default_sizes = {
            "sidebar": 250,
            "ai_panel": 350,
            "terminal": 150,
            "editor": -1  # Flexible
        }
        self.current_sizes = self.default_sizes.copy()
        self.min_sizes = {
            "sidebar": 50,
            "ai_panel": 200,
            "terminal": 100,
            "editor": 200
        }
        self.max_sizes = {
            "sidebar": 500,
            "ai_panel": 600,
            "terminal": 500,
            "editor": -1
        }
    
    def get_size(self, panel_name):
        """Get panel size"""
        return self.current_sizes.get(panel_name, self.default_sizes.get(panel_name, 100))
    
    def set_size(self, panel_name, size):
        """Set panel size with constraints"""
        min_size = self.min_sizes.get(panel_name, 0)
        max_size = self.max_sizes.get(panel_name, float('inf'))
        
        # Constrain size
        size = max(min_size, min(size, max_size))
        
        self.current_sizes[panel_name] = size
        return size
    
    def reset_to_default(self):
        """Reset all panels to default sizes"""
        self.current_sizes = self.default_sizes.copy()
    
    def save_layout(self):
        """Get current layout as dict"""
        return self.current_sizes.copy()
    
    def load_layout(self, layout):
        """Load layout from dict"""
        self.current_sizes.update(layout)
    
    def get_preset_layout(self, preset_name):
        """Get predefined layout"""
        presets = {
            "coding": {
                "sidebar": 250,
                "ai_panel": 300,
                "terminal": 150
            },
            "debugging": {
                "sidebar": 300,
                "ai_panel": 250,
                "terminal": 250
            },
            "ai_focus": {
                "sidebar": 200,
                "ai_panel": 500,
                "terminal": 100
            },
            "minimal": {
                "sidebar": 50,
                "ai_panel": 0,  # Hidden
                "terminal": 0   # Hidden
            }
        }
        return presets.get(preset_name, self.default_sizes)
