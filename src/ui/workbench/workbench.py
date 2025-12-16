"""
Workbench UI
The main window layout and component manager.
"""
import customtkinter as ctk
from src.services.theme_service import ThemeService
from src.core.container import get_service
from src.core.event_bus import global_event_bus
from src.ui.editor.code_editor import CodeEditor

from src.ui.views.explorer import ExplorerView
from src.ui.views.chat_view import ChatView
from src.ui.docking.dock_manager import DockingManager
from src.ui.widgets.terminal import Terminal
import os

class Workbench(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.theme = get_service("ThemeService")
        self.configure(fg_color=self.theme.get_color("bg_main"))
        
        
        # Layout Grid
        self.grid_columnconfigure(0, weight=0) # Activity Bar
        self.grid_columnconfigure(1, weight=0) # Sidebar
        self.grid_columnconfigure(2, weight=1) # Editor
        self.grid_columnconfigure(3, weight=0, minsize=300) # AI Panel
        
        self.grid_rowconfigure(0, weight=0, minsize=30) # Menu Bar
        self.grid_rowconfigure(1, weight=1) # Editor/Content height
        self.grid_rowconfigure(2, weight=0) # Status Bar
        self.grid_rowconfigure(3, weight=0) # Dock height
        
        # Components
        self._init_menu_bar()
        self._init_activity_bar()
        self._init_sidebar()
        self._init_editor_area()
        self._init_ai_panel()
        self._init_status_bar()
        
        # Docking System
        self.dock_manager = DockingManager(self)
        self.dock_manager.mount()
        self.terminal = self.dock_manager.add_bottom_panel("TERMINAL", Terminal)
        self.dock_manager.add_bottom_panel("OUTPUT", lambda m: ctk.CTkLabel(m, text="Build Output..."))
        
        
        # Events
        global_event_bus.subscribe("theme_changed", self.on_theme_changed)
        global_event_bus.subscribe("open_file", self.open_file_in_tab)

    def _init_menu_bar(self):
        """Initialize menu bar with File, Edit, View, Run, Terminal, Help"""
        from tkinter import Menu
        
        menu_frame = ctk.CTkFrame(self, height=30, fg_color="#303031", corner_radius=0)
        menu_frame.grid(row=0, column=0, columnspan=4, sticky="ew")
        
        # Menu buttons
        menus = {
            "File": self._show_file_menu,
            "Edit": self._show_edit_menu,
            "View": self._show_view_menu,
            "Run": self._show_run_menu,
            "Terminal": self._show_terminal_menu,
            "Help": self._show_help_menu
        }
        
        for name, command in menus.items():
            btn = ctk.CTkButton(
                menu_frame, 
                text=name, 
                fg_color="transparent", 
                width=50,
                hover_color="#3e3e42",
                command=command
            )
            btn.pack(side="left", padx=2)
        
        # Title label
        ctk.CTkLabel(
            menu_frame, 
            text="AI Fervv IDE - Galactic Edition", 
            text_color="gray"
        ).pack(side="right", padx=10)

    def _show_file_menu(self):
        from tkinter import Menu
        menu = Menu(self, tearoff=0)
        menu.add_command(label="New File (Ctrl+N)", command=lambda: global_event_bus.publish("new_file", None))
        menu.add_command(label="Open File (Ctrl+O)", command=lambda: global_event_bus.publish("open_file_dialog", None))
        menu.add_command(label="Save (Ctrl+S)", command=lambda: global_event_bus.publish("save_file", None))
        menu.add_separator()
        menu.add_command(label="Exit", command=self.master.quit)
        menu.post(self.winfo_pointerx(), self.winfo_pointery())

    def _show_edit_menu(self):
        from tkinter import Menu
        menu = Menu(self, tearoff=0)
        menu.add_command(label="Undo (Ctrl+Z)", command=lambda: global_event_bus.publish("undo", None))
        menu.add_command(label="Redo (Ctrl+Y)", command=lambda: global_event_bus.publish("redo", None))
        menu.add_separator()
        menu.add_command(label="Cut (Ctrl+X)", command=lambda: global_event_bus.publish("cut", None))
        menu.add_command(label="Copy (Ctrl+C)", command=lambda: global_event_bus.publish("copy", None))
        menu.add_command(label="Paste (Ctrl+V)", command=lambda: global_event_bus.publish("paste", None))
        menu.post(self.winfo_pointerx(), self.winfo_pointery())

    def _show_view_menu(self):
        from tkinter import Menu
        menu = Menu(self, tearoff=0)
        menu.add_command(label="Toggle Sidebar", command=self.toggle_sidebar)
        menu.add_command(label="Toggle Terminal", command=self.toggle_terminal)
        menu.add_separator()
        menu.add_command(label="Settings", command=lambda: global_event_bus.publish("open_settings", None))
        menu.post(self.winfo_pointerx(), self.winfo_pointery())

    def _show_run_menu(self):
        from tkinter import Menu
        menu = Menu(self, tearoff=0)
        menu.add_command(label="Run File (F5)", command=lambda: global_event_bus.publish("run_file", None))
        menu.post(self.winfo_pointerx(), self.winfo_pointery())

    def _show_terminal_menu(self):
        from tkinter import Menu
        menu = Menu(self, tearoff=0)
        menu.add_command(label="New Terminal", command=lambda: self.terminal.clear() if hasattr(self, 'terminal') else None)
        menu.add_command(label="Clear Terminal", command=lambda: self.terminal.clear() if hasattr(self, 'terminal') else None)
        menu.post(self.winfo_pointerx(), self.winfo_pointery())

    def _show_help_menu(self):
        from tkinter import Menu
        menu = Menu(self, tearoff=0)
        menu.add_command(label="About", command=self._show_about)
        menu.post(self.winfo_pointerx(), self.winfo_pointery())

    def _show_about(self):
        import customtkinter as ctk
        top = ctk.CTkToplevel(self)
        top.title("About")
        top.geometry("400x200")
        ctk.CTkLabel(top, text="AI Fervv IDE", font=("Segoe UI", 18, "bold")).pack(pady=20)
        ctk.CTkLabel(top, text="Galactic Edition", text_color="gray").pack()
        ctk.CTkLabel(top, text="Version: 2.0.0", text_color="gray").pack(pady=5)

    def toggle_sidebar(self):
        if self.sidebar_container.winfo_viewable():
            self.sidebar_container.grid_remove()
        else:
            self.sidebar_container.grid()

    def toggle_terminal(self):
        if hasattr(self, 'dock_manager'):
            # Toggle dock visibility
            pass  # Implement with DockingManager

    def _init_activity_bar(self):
        self.activity_bar = ctk.CTkFrame(self, width=50, corner_radius=0, fg_color=self.theme.get_color("bg_activity"))
        self.activity_bar.grid(row=1, column=0, sticky="ns", rowspan=3)
        
        # View switching buttons
        ctk.CTkButton(self.activity_bar, text="📁", width=40, height=40, fg_color="transparent",
                     command=lambda: self.switch_sidebar("explorer")).pack(pady=5)
        ctk.CTkButton(self.activity_bar, text="🔀", width=40, height=40, fg_color="transparent",
                     command=lambda: self.switch_sidebar("git")).pack(pady=5)
        ctk.CTkButton(self.activity_bar, text="📦", width=40, height=40, fg_color="transparent",
                     command=lambda: self.switch_sidebar("snippets")).pack(pady=5)
        ctk.CTkButton(self.activity_bar, text="✅", width=40, height=40, fg_color="transparent",
                     command=lambda: self.switch_sidebar("tasks")).pack(pady=5)
        
        # Settings Button
        ctk.CTkButton(self.activity_bar, text="⚙", width=40, height=40, fg_color="transparent",
                     command=lambda: global_event_bus.publish("open_settings", None)
                     ).pack(side="bottom", pady=10)

    def _init_sidebar(self):
        from src.ui.views.git_view import GitView
        from src.ui.views.snippets_view import SnippetsView
        from src.ui.views.tasks_view import TasksView
        
        self.sidebar_container = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color=self.theme.get_color("bg_sidebar"))
        self.sidebar_container.grid(row=1, column=1, sticky="ns")
        self.sidebar_container.grid_propagate(False) # Force width
        
        # All sidebar views
        self.explorer = ExplorerView(self.sidebar_container, fg_color="transparent")
        self.git_view = GitView(self.sidebar_container, fg_color="transparent")
        self.snippets_view = SnippetsView(self.sidebar_container, fg_color="transparent")
        self.tasks_view = TasksView(self.sidebar_container, fg_color="transparent")
        
        # Store views for switching
        self.sidebar_views = {
            "explorer": self.explorer,
            "git": self.git_view,
            "snippets": self.snippets_view,
            "tasks": self.tasks_view
        }
        
        # Show explorer by default
        self.explorer.pack(fill="both", expand=True)
        self.current_sidebar = "explorer"

    def switch_sidebar(self, mode):
        """Switch between sidebar views"""
        # Hide all views
        for view in self.sidebar_views.values():
            view.pack_forget()
        
        # Show selected view
        if mode in self.sidebar_views:
            self.sidebar_views[mode].pack(fill="both", expand=True)
            self.current_sidebar = mode

    def _init_editor_area(self):
        self.editor_tabs = ctk.CTkTabview(self, fg_color=self.theme.get_color("bg_main"), segmented_button_fg_color="#2d2d2d")
        self.editor_tabs.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        
        # Default Tab
        # self.open_file_in_tab(None) # Or start empty

    def _init_ai_panel(self):
        self.ai_panel = ctk.CTkFrame(self, width=300, corner_radius=0, fg_color=self.theme.get_color("bg_sidebar"))
        self.ai_panel.grid(row=1, column=3, sticky="ns", rowspan=3)
        self.ai_panel.grid_propagate(False)
        
        ctk.CTkLabel(self.ai_panel, text="AI ASSISTANT", font=("Segoe UI", 11, "bold"), text_color="gray").pack(anchor="w", padx=10, pady=10)
        
        self.chat_view = ChatView(self.ai_panel, fg_color="transparent")
        self.chat_view.pack(fill="both", expand=True)

    def open_file_in_tab(self, file_path):
        name = os.path.basename(file_path) if file_path else "Untitled"
        
        # Check if already open (simplified)
        try:
            self.editor_tabs.set(name)
            return
        except:
            pass # Not found, create new
            
        tab = self.editor_tabs.add(name)
        ext = name.split(".")[-1] if "." in name else "txt"
        editor = CodeEditor(tab, file_ext=ext, file_path=file_path)
        editor.pack(fill="both", expand=True)
        self.editor_tabs.set(name)

    def _init_status_bar(self):
        self.status_bar = ctk.CTkFrame(self, height=25, corner_radius=0, fg_color=self.theme.get_color("bg_status"))
        self.status_bar.grid(row=2, column=0, columnspan=4, sticky="ew") # Span 4 cols
        
        ctk.CTkLabel(self.status_bar, text="Ready", text_color="white", font=("Segoe UI", 11)).pack(side="left", padx=10)

    def on_theme_changed(self, theme):
        self.configure(fg_color=theme.colors.get("bg_main"))
