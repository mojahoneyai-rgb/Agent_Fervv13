"""
Explorer View
Tree-based project navigator using Tkinter Treeview.
"""
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import os
from src.core.event_bus import global_event_bus
from src.core.container import get_service

class ExplorerView(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.file_service = get_service("FileService")
        self.theme = get_service("ThemeService")
        self.current_path = os.getcwd()
        
        # UI Setup
        self.pack_propagate(False)
        self._init_tree()
        self.refresh()
        
        # Events
        global_event_bus.subscribe("file_saved", self._on_file_changed)

    def _init_tree(self):
        # We need a style for the Treeview to match Dark Mode
        style = ttk.Style()
        style.theme_use("default")
        
        bg = self.theme.get_color("bg_sidebar")
        fg = self.theme.get_color("fg_text")
        
        style.configure("Treeview", 
                        background=bg, 
                        foreground=fg, 
                        fieldbackground=bg,
                        borderwidth=0,
                        font=("Segoe UI", 10))
        style.map('Treeview', background=[('selected', '#37373d')])

        self.tree = ttk.Treeview(self, show="tree", selectmode="browse")
        self.tree.pack(fill="both", expand=True, padx=0, pady=0)
        
        # Scrollbar
        # scroll = ctk.CTkScrollbar(self, command=self.tree.yview)
        # scroll.pack(side="right", fill="y")
        # self.tree.configure(yscrollcommand=scroll.set)
        
        self.tree.bind("<<TreeviewSelect>>", self._on_select)
        self.tree.bind("<Double-1>", self._on_double_click)

    def refresh(self):
        """Rebuilds the tree from current path."""
        # Clear
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        # Add Root
        root_node = self.tree.insert("", "end", text=os.path.basename(self.current_path), open=True)
        self._populate_node(root_node, self.current_path)

    def _populate_node(self, parent_node, path):
        dirs, files = self.file_service.list_files(path)
        
        for d in dirs:
            full_path = os.path.join(path, d)
            node = self.tree.insert(parent_node, "end", text=f"📁 {d}", values=[full_path])
            # For deeper recursion we could lazy load, but for now just 1 level or full? 
            # Let's do 1 level deep to verify it works
            # self._populate_node(node, full_path) 
            
        for f in files:
            full_path = os.path.join(path, f)
            self.tree.insert(parent_node, "end", text=f"📄 {f}", values=[full_path])

    def _on_event(self, event):
        pass

    def _on_select(self, event):
        pass

    def _on_double_click(self, event):
        item = self.tree.selection()[0]
        values = self.tree.item(item, "values")
        if values:
            path = values[0]
            if os.path.isfile(path):
                global_event_bus.publish("open_file", path)
            elif os.path.isdir(path):
                # Optionally toggle open/close
                pass

    def _on_file_changed(self, path):
        # self.refresh() # Simplified
        pass
