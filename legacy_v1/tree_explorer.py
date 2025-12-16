"""
AI Fervv IDE - Advanced TreeView File Explorer
VS Code-style file tree with expandable folders
"""

import customtkinter as ctk
import os
from tkinter import PhotoImage
from file_icons import get_file_icon

class FileTreeItem(ctk.CTkFrame):
    """Single file/folder item in tree"""
    
    def __init__(self, master, path, name, is_dir, level=0, on_click=None, on_expand=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.path = path
        self.name = name
        self.is_dir = is_dir
        self.level = level
        self.on_click = on_click
        self.on_expand = on_expand
        self.expanded = False
        self.children_frame = None
        
        # Main container
        self.item_frame = ctk.CTkFrame(self, fg_color="transparent", height=24)
        self.item_frame.pack(fill="x")
        
        # Indent based on level
        indent = 12 * level
        if indent > 0:
            ctk.CTkLabel(self.item_frame, text="", width=indent).pack(side="left")
        
        # Expand/collapse arrow for directories
        if self.is_dir:
            self.arrow_label = ctk.CTkLabel(
                self.item_frame, text="▶", width=15, font=("Segoe UI", 10)
            )
            self.arrow_label.pack(side="left")
            self.arrow_label.bind("<Button-1>", self.toggle_expand)
        else:
            ctk.CTkLabel(self.item_frame, text="", width=15).pack(side="left")
        
        # Icon
        icon = get_file_icon(name, is_directory=is_dir)
        ctk.CTkLabel(self.item_frame, text=icon, width=20, font=("Segoe UI", 12)).pack(side="left")
        
        # Name label
        self.name_label = ctk.CTkLabel(
            self.item_frame, text=name, anchor="w",
            font=("Segoe UI", 10), text_color="#cccccc"
        )
        self.name_label.pack(side="left", fill="x", expand=True, padx=2)
        
        # Click events
        if not self.is_dir and on_click:
            self.name_label.bind("<Button-1>", lambda e: on_click(self.path))
            self.name_label.bind("<Enter>", lambda e: self.name_label.configure(text_color="#ffffff"))
            self.name_label.bind("<Leave>", lambda e: self.name_label.configure(text_color="#cccccc"))
    
    def toggle_expand(self, event=None):
        """Toggle folder expansion"""
        if not self.is_dir:
            return
        
        self.expanded = not self.expanded
        
        if self.expanded:
            self.arrow_label.configure(text="▼")
            if self.on_expand:
                self.on_expand(self)
        else:
            self.arrow_label.configure(text="▶")
            if self.children_frame:
                self.children_frame.destroy()
                self.children_frame = None
    
    def add_children(self, children_frame):
        """Add children container"""
        self.children_frame = children_frame
        self.children_frame.pack(fill="x", after=self.item_frame)

class TreeViewExplorer(ctk.CTkScrollableFrame):
    """VS Code-style file tree explorer"""
    
    def __init__(self, master, on_file_click=None, **kwargs):
        super().__init__(master, fg_color="transparent", **kwargs)
        
        self.on_file_click = on_file_click
        self.current_folder = None
        self.tree_items = {}  # path -> TreeItem
        
    def load_folder(self, folder_path):
        """Load folder structure"""
        self.current_folder = folder_path
        
        # Clear existing
        for widget in self.winfo_children():
            widget.destroy()
        self.tree_items.clear()
        
        if not folder_path or not os.path.exists(folder_path):
            return
        
        # Load root level
        self._load_directory_contents(folder_path, self, level=0)
    
    def _load_directory_contents(self, dir_path, parent_widget, level=0):
        """Load contents of a directory"""
        try:
            items = os.listdir(dir_path)
            
            # Separate and sort: directories first, then files
            dirs = []
            files = []
            
            for item in items:
                if item.startswith('.'):  # Skip hidden files
                    continue
                
                full_path = os.path.join(dir_path, item)
                if os.path.isdir(full_path):
                    dirs.append((item, full_path))
                else:
                    files.append((item, full_path))
            
            dirs.sort(key=lambda x: x[0].lower())
            files.sort(key=lambda x: x[0].lower())
            
            # Create directory items
            for name, path in dirs:
                item = FileTreeItem(
                    parent_widget,
                    path=path,
                    name=name,
                    is_dir=True,
                    level=level,
                    on_expand=self._on_expand_folder
                )
                item.pack(fill="x", pady=1)
                self.tree_items[path] = item
            
            # Create file items
            for name, path in files:
                item = FileTreeItem(
                    parent_widget,
                    path=path,
                    name=name,
                    is_dir=False,
                    level=level,
                    on_click=self.on_file_click
                )
                item.pack(fill="x", pady=1)
                self.tree_items[path] = item
                
        except Exception as e:
            print(f"Error loading directory: {e}")
    
    def _on_expand_folder(self, tree_item):
        """Handle folder expansion"""
        if tree_item.expanded:
            # Create children container
            children_frame = ctk.CTkFrame(tree_item, fg_color="transparent")
            tree_item.add_children(children_frame)
            
            # Load folder contents
            self._load_directory_contents(
                tree_item.path,
                children_frame,
                level=tree_item.level + 1
            )
    
    def refresh(self):
        """Refresh current folder"""
        if self.current_folder:
            self.load_folder(self.current_folder)
