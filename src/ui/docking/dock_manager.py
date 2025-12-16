"""
Docking System
Manages panels (Terminal, Explorer, Output) in a flexible layout.
"""
import customtkinter as ctk

class DockingManager:
    def __init__(self, master_frame):
        self.master = master_frame
        self.panels = {}
        
        # Bottom Panel (Terminal/Output)
        self.bottom_pane = ctk.CTkTabview(master_frame, height=200, fg_color="transparent")
        # Start hidden or collapsed logic? For now strict grid.
        
    def setup_layout(self):
        # Already handled by Workbench grid basically.
        # This class would handle drag/drop reordering in V2.
        pass

    def add_bottom_panel(self, title, widget_class):
        self.bottom_pane.add(title)
        widget = widget_class(self.bottom_pane.tab(title))
        widget.pack(fill="both", expand=True)
        return widget

    def mount(self):
        """Mounts the bottom dock to the master grid"""
        # Assuming Workbench Grid
        self.bottom_pane.grid(row=2, column=1, columnspan=2, sticky="ew")
