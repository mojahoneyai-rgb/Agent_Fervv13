"""
Professional Menu System for AI Fervv IDE
Complete VS Code-style menus with all functionality
"""

import customtkinter as ctk
from tkinter import Menu

class ProfessionalMenu:
    """Professional menu bar with full functionality"""
    
    def __init__(self, parent_ide):
        self.ide = parent_ide
        self.menubar = Menu(parent_ide, bg="#2d2d2d", fg="#cccccc", 
                          activebackground="#007ACC", activeforeground="white",
                          tearoff=0)
        parent_ide.config(menu=self.menubar)
        
        self.create_file_menu()
        self.create_edit_menu()
        self.create_selection_menu()
        self.create_view_menu()
        self.create_go_menu()
        self.create_run_menu()
        self.create_terminal_menu()
        self.create_help_menu()
    
    def create_file_menu(self):
        """File menu - complete VS Code style"""
        file_menu = Menu(self.menubar, tearoff=0, bg="#2d2d2d", fg="#cccccc")
        
        file_menu.add_command(label="New File", accelerator="Ctrl+N",
                            command=self.ide.new_file)
        file_menu.add_command(label="New Window", accelerator="Ctrl+Shift+N",
                            command=self.ide.new_window)
        file_menu.add_separator()
        file_menu.add_command(label="Open File...", accelerator="Ctrl+O",
                            command=self.ide.open_file_dialog)
        file_menu.add_command(label="Open Folder...", accelerator="Ctrl+K Ctrl+O",
                            command=self.ide.open_folder_dialog)
        file_menu.add_command(label="Open Workspace...",
                            command=self.ide.open_workspace)
        file_menu.add_separator()
        file_menu.add_command(label="Save", accelerator="Ctrl+S",
                            command=self.ide.save_file)
        file_menu.add_command(label="Save As...", accelerator="Ctrl+Shift+S",
                            command=self.ide.save_as)
        file_menu.add_command(label="Save All", accelerator="Ctrl+K S",
                            command=self.ide.save_all)
        file_menu.add_separator()
        file_menu.add_checkbutton(label="Auto Save", 
                                 command=self.ide.toggle_autosave)
        file_menu.add_separator()
        file_menu.add_cascade(label="Preferences", menu=self.create_preferences_menu())
        file_menu.add_separator()
        file_menu.add_command(label="Revert File",
                            command=self.ide.revert_file)
        file_menu.add_command(label="Close Editor", accelerator="Ctrl+W",
                            command=self.ide.close_current_tab)
        file_menu.add_command(label="Close Folder",
                            command=self.ide.close_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Alt+F4",
                            command=self.ide.quit)
        
        self.menubar.add_cascade(label="File", menu=file_menu)
    
    def create_preferences_menu(self):
        """Preferences submenu"""
        pref_menu = Menu(self.menubar, tearoff=0, bg="#2d2d2d", fg="#cccccc")
        pref_menu.add_command(label="Settings", accelerator="Ctrl+,",
                            command=self.ide.show_settings)
        pref_menu.add_command(label="Extensions",
                            command=lambda: self.ide.switch_sidebar("extensions"))
        pref_menu.add_command(label="Keyboard Shortcuts",
                            command=self.ide.show_shortcuts)
        pref_menu.add_separator()
        
        # Font Size Submenu
        font_size_menu = Menu(pref_menu, tearoff=0, bg="#2d2d2d", fg="#cccccc")
        font_size_menu.add_command(label="Increase", accelerator="Ctrl++",
                                 command=lambda: self.ide.set_font_size(self.ide.font_size + 2))
        font_size_menu.add_command(label="Decrease", accelerator="Ctrl+-",
                                 command=lambda: self.ide.set_font_size(max(8, self.ide.font_size - 2)))
        font_size_menu.add_separator()
        for size in [10, 12, 14, 16, 18, 20, 24]:
            font_size_menu.add_command(label=f"{size} px",
                                     command=lambda s=size: self.ide.set_font_size(s))
        pref_menu.add_cascade(label="Font Size", menu=font_size_menu)

        # Font Family Submenu
        font_fam_menu = Menu(pref_menu, tearoff=0, bg="#2d2d2d", fg="#cccccc")
        fonts = ["Consolas", "Cascadia Code", "Courier New", "JetBrains Mono", "Source Code Pro", "Arial"]
        for font in fonts:
            font_fam_menu.add_command(label=font,
                                    command=lambda f=font: self.ide.set_font_family(f))
        pref_menu.add_cascade(label="Font Family", menu=font_fam_menu)

        pref_menu.add_separator()
        pref_menu.add_command(label="Color Theme",
                            command=self.ide.show_theme_selector)
        return pref_menu
    
    def create_edit_menu(self):
        """Edit menu"""
        edit_menu = Menu(self.menubar, tearoff=0, bg="#2d2d2d", fg="#cccccc")
        
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z",
                            command=self.ide.undo)
        edit_menu.add_command(label="Redo", accelerator="Ctrl+Y",
                            command=self.ide.redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X",
                            command=self.ide.cut)
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C",
                            command=self.ide.copy)
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V",
                            command=self.ide.paste)
        edit_menu.add_separator()
        edit_menu.add_command(label="Find", accelerator="Ctrl+F",
                            command=self.ide.show_find_dialog)
        edit_menu.add_command(label="Replace", accelerator="Ctrl+H",
                            command=self.ide.show_replace_dialog)
        
        self.menubar.add_cascade(label="Edit", menu=edit_menu)
    
    def create_selection_menu(self):
        """Selection menu"""
        sel_menu = Menu(self.menubar, tearoff=0, bg="#2d2d2d", fg="#cccccc")
        
        sel_menu.add_command(label="Select All", accelerator="Ctrl+A",
                           command=self.ide.select_all)
        sel_menu.add_command(label="Expand Selection",
                           command=lambda: None)  # TODO
        sel_menu.add_command(label="Shrink Selection",
                           command=lambda: None)  # TODO
        
        self.menubar.add_cascade(label="Selection", menu=sel_menu)
    
    def create_view_menu(self):
        """View menu"""
        view_menu = Menu(self.menubar, tearoff=0, bg="#2d2d2d", fg="#cccccc")
        
        view_menu.add_command(label="Command Palette", accelerator="Ctrl+Shift+P",
                            command=self.ide.show_command_palette)
        view_menu.add_separator()
        view_menu.add_checkbutton(label="Explorer",
                                command=lambda: self.ide.switch_sidebar("explorer"))
        view_menu.add_checkbutton(label="Git",
                                command=lambda: self.ide.switch_sidebar("git"))
        view_menu.add_checkbutton(label="Extensions",
                                command=lambda: self.ide.switch_sidebar("extensions"))
        view_menu.add_separator()
        view_menu.add_checkbutton(label="Terminal", accelerator="Ctrl+`",
                                command=self.ide.toggle_terminal)
        view_menu.add_checkbutton(label="AI Panel",
                                command=self.ide.toggle_ai_panel)
        view_menu.add_separator()
        view_menu.add_command(label="Toggle Fullscreen", accelerator="F11",
                            command=self.ide.toggle_fullscreen)
        
        self.menubar.add_cascade(label="View", menu=view_menu)
    
    def create_go_menu(self):
        """Go menu"""
        go_menu = Menu(self.menubar, tearoff=0, bg="#2d2d2d", fg="#cccccc")
        
        go_menu.add_command(label="Go to File...", accelerator="Ctrl+P",
                          command=self.ide.show_command_palette)
        go_menu.add_command(label="Go to Line...", accelerator="Ctrl+G",
                          command=self.ide.go_to_line)
        
        self.menubar.add_cascade(label="Go", menu=go_menu)
    
    def create_run_menu(self):
        """Run menu"""
        run_menu = Menu(self.menubar, tearoff=0, bg="#2d2d2d", fg="#cccccc")
        
        run_menu.add_command(label="Run Python File", accelerator="Ctrl+F5",
                           command=self.ide.run_with_python)
        run_menu.add_command(label="Run Build Task",
                           command=self.ide.run_build_task)
        run_menu.add_separator()
        run_menu.add_command(label="Configure Tasks...",
                           command=self.ide.configure_tasks)
        
        self.menubar.add_cascade(label="Run", menu=run_menu)
    
    def create_terminal_menu(self):
        """Terminal menu - complete from user image"""
        term_menu = Menu(self.menubar, tearoff=0, bg="#2d2d2d", fg="#cccccc")
        
        term_menu.add_command(label="New Terminal", accelerator="Ctrl+Shift+`",
                            command=self.ide.new_terminal)
        term_menu.add_command(label="Split Terminal",
                            command=self.ide.split_terminal)
        term_menu.add_separator()
        term_menu.add_command(label="Run Build Task", accelerator="Ctrl+Shift+B",
                            command=self.ide.run_build_task)
        term_menu.add_command(label="Run Active File",
                            command=self.ide.run_with_python)
        term_menu.add_separator()
        term_menu.add_command(label="Configure Default Build Task...",
                            command=self.ide.configure_build_task)
        term_menu.add_command(label="Configure Tasks...",
                            command=self.ide.configure_tasks)
        term_menu.add_separator()
        term_menu.add_command(label="Show Running Tasks...",
                            command=self.ide.show_running_tasks)
        term_menu.add_command(label="Restart Running Task...",
                            command=self.ide.restart_task)
        term_menu.add_command(label="Terminate Task...",
                            command=self.ide.terminate_task)
        
        self.menubar.add_cascade(label="Terminal", menu=term_menu)
    
    def create_help_menu(self):
        """Help menu"""
        help_menu = Menu(self.menubar, tearoff=0, bg="#2d2d2d", fg="#cccccc")
        
        help_menu.add_command(label="Welcome",
                            command=self.ide.show_welcome)
        help_menu.add_command(label="Keyboard Shortcuts Reference",
                            command=self.ide.show_shortcuts)
        help_menu.add_separator()
        help_menu.add_command(label="About",
                            command=self.ide.show_about)
        
        self.menubar.add_cascade(label="Help", menu=help_menu)
