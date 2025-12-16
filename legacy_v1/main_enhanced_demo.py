# AI Fervv IDE - Complete Enhanced Version
# Full integration of all advanced features

"""
COMPLETE FEATURE LIST:
- AI Status Display (Myśli/Szuka/Pisze)
- Task Manager with priorities
- Full menu system (File/Edit/View/Run/Terminal/Help)
- Clipboard operations (Cut/Copy/Paste)
- Undo/Redo system
- Enhanced Live Logs
- Better AI chat interface
- All existing features from previous version

NOTE: This is a demonstration/starter version showing key integrations.
Some advanced features like resizable panels and streaming AI require
more complex implementation and are marked as TODO.
"""

import customtkinter as ctk
from agent import AI_Fervv
import threading
import os
import subprocess
import re
import json
import datetime
from tkinter import filedialog, END, Toplevel, Listbox, Menu, simpledialog, messagebox
from themes import ThemeManager, THEMES
from snippets import SnippetManager
from git_manager import GitManager
from autocomplete import AutocompleteEngine
from project_templates import TemplateManager
from file_icons import get_file_icon, get_language_from_extension
from ai_status import AIStatusManager, AgentStatus, status_manager
from clipboard_manager import ClipboardManager, UndoRedoManager
from task_manager import TaskManager, TaskPriority, TaskStatus as TaskStatusEnum
from panel_manager import PanelManager

# --- GLOBAL THEME MANAGER ---
theme_manager = ThemeManager()

def COLORS(key):
    """Get color from current theme"""
    return theme_manager.get_color(key)

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# --- SYNTAX HIGHLIGHTING ---
class SyntaxHighlighter:
    def __init__(self, text_widget, lang="python"):
        self.text_widget = text_widget
        self.lang = lang
        self.setup_tags()

    def setup_tags(self):
        tb = self.text_widget._textbox
        tb.tag_config("keyword", foreground=COLORS("fg_keyword"))
        tb.tag_config("comment", foreground=COLORS("fg_comment"))
        tb.tag_config("string", foreground=COLORS("fg_string"))
        tb.tag_config("function", foreground=COLORS("fg_function"))
        tb.tag_config("number", foreground=COLORS("fg_number"))

    def highlight(self, event=None):
        content = self.text_widget.get("1.0", "end-1c")
        tb = self.text_widget._textbox
        
        for tag in ["keyword", "comment", "string", "function", "number"]:
            tb.tag_remove(tag, "1.0", "end")

        if self.lang == "python":
            self.highlight_python(content)
        elif self.lang == "json":
            self.highlight_json(content)
        elif self.lang == "css":
            self.highlight_css(content)

    def highlight_python(self, content):
        keywords = ["def", "class", "import", "from", "return", "if", "else", "elif", "while", "for", "in", "try", "except", "print", "self", "True", "False", "None", "with", "as", "global", "pass", "break", "continue"]
        pattern_kw = r"\b(" + "|".join(keywords) + r")\b"
        self.apply_tag(pattern_kw, "keyword")
        self.apply_tag(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)", "function")
        self.apply_tag(r'(\".*?\"|\'.*?\')', "string")
        self.apply_tag(r"(#.*?$)", "comment")
        self.apply_tag(r"\b\d+\b", "number")

    def highlight_json(self, content):
        self.apply_tag(r'(\".*?\")\\s*:', "keyword")
        self.apply_tag(r':\\s*(\".*?\")', "string")
        self.apply_tag(r"\b\d+\b", "number")
        self.apply_tag(r"\b(true|false|null)\b", "keyword")

    def highlight_css(self, content):
        self.apply_tag(r"([a-zA-Z0-9\\-_]+)(?=\\s*\\{)", "function")
        self.apply_tag(r"([a-zA-Z0-9\\-_]+)(?=:)", "keyword")
        self.apply_tag(r":\\s*([^;]+);", "string")
        self.apply_tag(r"/\\*.*?\\*/", "comment")

    def apply_tag(self, pattern, tag):
        count = ctk.StringVar()
        self.text_widget._textbox.mark_set("searchLimit", "end")
        self.text_widget._textbox.mark_set("matchStart", "1.0")
        
        while True:
            pos = self.text_widget._textbox.search(pattern, "matchStart", stopindex="end", count=count, regexp=True)
            if not pos: break
            self.text_widget._textbox.mark_set("matchStart", pos)
            self.text_widget._textbox.mark_set("matchEnd", f"{pos}+{count.get()}c")
            self.text_widget._textbox.tag_add(tag, "matchStart", "matchEnd")
            self.text_widget._textbox.mark_set("matchStart", "matchEnd")

# --- CUSTOM EDITOR WIDGET ---
class CodeEditor(ctk.CTkFrame):
    def __init__(self, master, font_size=14, file_ext=".py", **kwargs):
        super().__init__(master, fg_color=COLORS("bg_main"), **kwargs)
        self.autocomplete_engine = AutocompleteEngine()
        self.autocomplete_window = None
        self.file_ext = file_ext
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Line Numbers
        self.line_numbers = ctk.CTkTextbox(
            self, width=40, font=("Consolas", font_size),
            fg_color=COLORS("line_num_bg"), text_color=COLORS("line_num_fg"),
            activate_scrollbars=False
        )
        self.line_numbers.grid(row=0, column=0, sticky="ns")
        self.line_numbers.insert("1.0", "1")
        self.line_numbers.configure(state="disabled")
        
        # Main Textbox
        self.textbox = ctk.CTkTextbox(
            self, wrap="none", font=("Consolas", font_size), undo=True,
            fg_color=COLORS("bg_main"), text_color=COLORS("fg_text"),
            activate_scrollbars=True
        )
        self.textbox.grid(row=0, column=1, sticky="nsew")
        
        # Sync scrolling
        self.textbox._textbox.configure(yscrollcommand=self.on_text_scroll)
        self.line_numbers._textbox.configure(yscrollcommand=self.on_ln_scroll)

        lang = "python"
        if file_ext.endswith(".json"): lang = "json"
        elif file_ext.endswith(".css"): lang = "css"
        elif file_ext.endswith(".js"): lang = "python"
        
        self.highlighter = SyntaxHighlighter(self.textbox, lang)
        
        self.textbox.bind("<KeyRelease>", self.on_key_release)
        self.textbox.bind("<Button-1>", self.on_click)
        self.textbox.bind("<MouseWheel>", self.on_mouse_wheel)

    def on_text_scroll(self, *args):
        self.line_numbers.yview_moveto(args[0])

    def on_ln_scroll(self, *args):
        self.textbox.yview_moveto(args[0])

    def on_mouse_wheel(self, event):
        self.line_numbers.yview_scroll(int(-1*(event.delta/120)), "units")
        self.textbox.yview_scroll(int(-1*(event.delta/120)), "units")
        return "break"

    def on_key_release(self, event=None):
        self.highlighter.highlight()
        self.update_line_numbers()
        
    def on_click(self, event=None):
        self.update_line_numbers()

    def update_line_numbers(self):
        lines = self.textbox.get("1.0", "end-1c").split("\n")
        line_count = len(lines)
        if line_count == 0: line_count = 1
        
        current_content = self.line_numbers.get("1.0", "end-1c")
        new_nums = "\n".join(str(i) for i in range(1, line_count + 1))
        
        if current_content.strip() != new_nums.strip():
            self.line_numbers.configure(state="normal")
            self.line_numbers.delete("1.0", "end")
            self.line_numbers.insert("1.0", new_nums)
            self.line_numbers.configure(state="disabled")
            
        self.line_numbers.yview_moveto(self.textbox.yview()[0])
        
    def get_text(self):
        return self.textbox.get("1.0", "end-1c")

    def set_text(self, text):
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", text)
        self.highlighter.highlight()
        self.update_line_numbers()

    def append_text(self, text):
        self.textbox.insert("end", text)
        self.textbox.see("end")
        self.update_line_numbers()

# === MAIN APPLICATION ===
class FervvIDE(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # State
        self.current_folder = None
        self.open_documents = {}
        self.current_file_path = None
        self.agent = AI_Fervv()
        self.active_sidebar = "explorer"
        self.sidebar_visible = True
        
        # Managers
        self.snippet_manager = SnippetManager()
        self.git_manager = GitManager()
        self.template_manager = TemplateManager()
        self.autocomplete_engine = AutocompleteEngine()
        self.ai_status_manager = status_manager
        self.clipboard_manager = ClipboardManager()
        self.task_manager = TaskManager()
        self.panel_manager = PanelManager()
        self.undo_managers = {}

        # UI Config
        self.title("AI Fervv Studio Code - Complete Enhanced Edition 🚀✨")
        self.geometry("1400x900")
        self.configure(fg_color=COLORS("bg_main"))
        
        # Grid
        self.grid_columnconfigure(0, weight=0, minsize=50)
        self.grid_columnconfigure(1, weight=0, minsize=250)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=0, minsize=350)
        self.grid_rowconfigure(0, weight=0, minsize=30)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0, minsize=25)

        self.setup_menu()
        self.setup_activity_bar()
        self.setup_sidebars()
        self.setup_editor()
        self.setup_ai_panel()
        self.setup_status_bar()

        # Enhanced Keyboard Shortcuts
        self.bind("<Control-s>", self.save_file)
        self.bind("<Control-n>", lambda e: self.new_file())
        self.bind("<Control-o>", lambda e: self.open_file_dialog())
        self.bind("<Control-w>", lambda e: self.close_current_tab())
        self.bind("<Control-p>", self.show_command_palette)
        self.bind("<Control-b>", self.toggle_sidebar)
        self.bind("<Control-Shift-p>", self.show_project_templates)
        self.bind("<Control-Shift-t>", self.show_theme_selector)
        self.bind("<Control-Shift-s>", self.show_snippets_quick_insert)
        self.bind("<Control-comma>", self.show_settings)
        # Edit operations
        self.bind("<Control-z>", self.undo)
        self.bind("<Control-y>", self.redo)
        self.bind("<Control-x>", self.cut)
        self.bind("<Control-c>", self.copy)
        self.bind("<Control-v>", self.paste)
        self.bind("<Control-a>", self.select_all)
        self.bind("<Control-f>", self.show_find_dialog)
        self.bind("<F5>", self.run_file)

        # Boot
        self.create_tab("🔴 Live Logs")
        self.set_tab_content("🔴 Live Logs", f"# AI FERVV IDE - ENHANCED SYSTEM LOGS\n# Started: {datetime.datetime.now().strftime('%H:%M:%S')}\n" + "="*60 + "\n")

        # Load settings
        self.load_settings()

        # Fade in
        self.attributes("-alpha", 0.0)
        self.after(100, self.animate_fade_in)
        
        # Register AI status callback
        self.ai_status_manager.register_callback(self.on_ai_status_change)

    def animate_fade_in(self, current_alpha=0.0):
        if current_alpha < 1.0:
            current_alpha += 0.05
            self.attributes("-alpha", current_alpha)
            self.after(20, lambda: self.animate_fade_in(current_alpha))
        else:
            self.attributes("-alpha", 1.0)

    # === MENU SYSTEM ===
    def setup_menu(self):
        """Enhanced menu bar with working functions"""
        mf = ctk.CTkFrame(self, height=30, fg_color="#303031", corner_radius=0)
        mf.grid(row=0, column=0, columnspan=4, sticky="ew")
        
        # Create menu buttons
        menus = {
            "File": self.show_file_menu,
            "Edit": self.show_edit_menu,
            "Selection": self.show_selection_menu,
            "View": self.show_view_menu,
            "Go": self.show_go_menu,
            "Run": self.show_run_menu,
            "Terminal": self.show_terminal_menu,
            "Help": self.show_help_menu
        }
        
        for name, command in menus.items():
            ctk.CTkButton(mf, text=name, fg_color="transparent", width=50, 
                         hover_color=COLORS("hover"), command=command).pack(side="left", padx=2)
        
        ctk.CTkLabel(mf, text="AI Fervv Studio - Complete Edition", 
                    text_color="gray").pack(side="right", padx=10)

    def show_file_menu(self):
        menu = Menu(self, tearoff=0)
        menu.add_command(label="New File (Ctrl+N)", command=self.new_file)
        menu.add_command(label="Open File (Ctrl+O)", command=self.open_file_dialog)
        menu.add_command(label="Save (Ctrl+S)", command=lambda: self.save_file())
        menu.add_command(label="Save As", command=self.save_as)
        menu.add_separator()
        menu.add_command(label="Close Tab (Ctrl+W)", command=self.close_current_tab)
        menu.add_separator()
        menu.add_command(label="Exit", command=self.quit)
        menu.post(self.winfo_pointerx(), self.winfo_pointery())

    def show_edit_menu(self):
        menu = Menu(self, tearoff=0)
        menu.add_command(label="Undo (Ctrl+Z)", command=lambda: self.undo())
        menu.add_command(label="Redo (Ctrl+Y)", command=lambda: self.redo())
        menu.add_separator()
        menu.add_command(label="Cut (Ctrl+X)", command=lambda: self.cut())
        menu.add_command(label="Copy (Ctrl+C)", command=lambda: self.copy())
        menu.add_command(label="Paste (Ctrl+V)", command=lambda: self.paste())
        menu.add_separator()
        menu.add_command(label="Select All (Ctrl+A)", command=lambda: self.select_all())
        menu.add_separator()
        menu.add_command(label="Find (Ctrl+F)", command=lambda: self.show_find_dialog())
        menu.post(self.winfo_pointerx(), self.winfo_pointery())

    def show_selection_menu(self):
        menu = Menu(self, tearoff=0)
        menu.add_command(label="Select All", command=lambda: self.select_all())
        menu.add_command(label="Expand Selection", command=lambda: self.chat_append("System", "Expand selection - TODO"))
        menu.post(self.winfo_pointerx(), self.winfo_pointery())

    def show_view_menu(self):
        menu = Menu(self, tearoff=0)
        menu.add_command(label="Toggle Sidebar (Ctrl+B)", command=lambda: self.toggle_sidebar())
        menu.add_command(label="Toggle Terminal", command=self.toggle_terminal)
        menu.add_command(label="Toggle AI Panel", command=self.toggle_ai_panel)
        menu.add_separator()
        menu.add_command(label="Zoom In", command=lambda: self.chat_append("System", "Zoom - TODO"))
        menu.add_command(label="Zoom Out", command=lambda: self.chat_append("System", "Zoom - TODO"))
        menu.post(self.winfo_pointerx(), self.winfo_pointery())

    def show_go_menu(self):
        menu = Menu(self, tearoff=0)
        menu.add_command(label="Go to File (Ctrl+P)", command=lambda: self.show_command_palette())
        menu.add_command(label="Go to Line", command=self.go_to_line)
        menu.post(self.winfo_pointerx(), self.winfo_pointery())

    def show_run_menu(self):
        menu = Menu(self, tearoff=0)
        menu.add_command(label="Run File (F5)", command=lambda: self.run_file())
        menu.add_command(label="Run with Python", command=self.run_with_python)
        menu.post(self.winfo_pointerx(), self.winfo_pointery())

    def show_terminal_menu(self):
        menu = Menu(self, tearoff=0)
        menu.add_command(label="New Terminal", command=lambda: self.chat_append("System", "New terminal - TODO"))
        menu.add_command(label="Clear Terminal", command=self.clear_terminal)
        menu.post(self.winfo_pointerx(), self.winfo_pointery())

    def show_help_menu(self):
        menu = Menu(self, tearoff=0)
        menu.add_command(label="Keyboard Shortcuts", command=self.show_shortcuts)
        menu.add_command(label="About", command=self.show_about)
        menu.post(self.winfo_pointerx(), self.winfo_pointery())

    # === UI SETUP (continued in next message due to length) ===
    
    def setup_activity_bar(self):
        f = ctk.CTkFrame(self, width=50, fg_color=COLORS("bg_activity"), corner_radius=0)
        f.grid(row=1, column=0, sticky="nsew")
        
        self.create_activity_btn(f, "📄", "explorer")
        self.create_activity_btn(f, "🔀", "git")
        self.create_activity_btn(f, "📦", "snippets")
        self.create_activity_btn(f, "✅", "tasks")  # NEW: Tasks
        self.create_activity_btn(f, "🧩", "extensions")
        
        ctk.CTkButton(f, text="⚙", width=40, font=("Arial", 20), 
                     fg_color="transparent",command=lambda: self.show_settings(None)).pack(side="bottom", pady=10)

    def create_activity_btn(self, parent, icon, mode):
        ctk.CTkButton(
            parent, text=icon, width=40, height=40, 
            fg_color="transparent", font=("Arial", 20), hover_color=COLORS("hover"),
            command=lambda: self.switch_sidebar(mode)
        ).pack(pady=5)

    def setup_sidebars(self):
        self.sidebar_container = ctk.CTkFrame(self, width=250, fg_color=COLORS("bg_sidebar"), corner_radius=0)
        self.sidebar_container.grid(row=1, column=1, sticky="nsew")
        self.sidebar_container.pack_propagate(False)
        
        # 1. EXPLORER
        self.explorer_frame = ctk.CTkFrame(self.sidebar_container, fg_color="transparent")
        h = ctk.CTkFrame(self.explorer_frame, height=30, fg_color="transparent")
        h.pack(fill="x")
        ctk.CTkLabel(h, text="EXPLORER", font=("Segoe UI", 11, "bold")).pack(side="left", padx=10)
        
        act = ctk.CTkFrame(self.explorer_frame, fg_color="transparent")
        act.pack(fill="x", padx=5, pady=5)
        ctk.CTkButton(act, text="Open Folder", width=110, height=24, 
                     command=self.open_folder_dialog).pack(side="left", padx=2)
        ctk.CTkButton(act, text="Refresh", width=60, height=24, 
                     command=self.refresh_explorer).pack(side="left", padx=2)

        self.file_list = ctk.CTkScrollableFrame(self.explorer_frame, fg_color="transparent")
        self.file_list.pack(fill="both", expand=True)
        
        # 2. GIT (existing code...)
        self.git_frame = ctk.CTkFrame(self.sidebar_container, fg_color="transparent")
        ctk.CTkLabel(self.git_frame, text="SOURCE CONTROL", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=10, pady=5)
        git_actions = ctk.CTkFrame(self.git_frame, fg_color="transparent")
        git_actions.pack(fill="x", padx=5, pady=5)
        ctk.CTkButton(git_actions, text="Init Repo", width=80, height=24, command=self.git_init).pack(side="left", padx=2)
        ctk.CTkButton(git_actions, text="Refresh", width=60, height=24, command=self.git_refresh_status).pack(side="left", padx=2)
        self.git_status_list = ctk.CTkScrollableFrame(self.git_frame, fg_color="transparent")
        self.git_status_list.pack(fill="both", expand=True, pady=5)
        git_commit_frame = ctk.CTkFrame(self.git_frame, fg_color="transparent")
        git_commit_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(git_commit_frame, text="Commit:", font=("Segoe UI", 10)).pack(anchor="w")
        self.git_commit_msg = ctk.CTkEntry(git_commit_frame, placeholder_text="Message...")
        self.git_commit_msg.pack(fill="x", pady=2)
        git_btn_frame = ctk.CTkFrame(git_commit_frame, fg_color="transparent")
        git_btn_frame.pack(fill="x", pady=2)
        ctk.CTkButton(git_btn_frame, text="Commit", width=70, height=24, command=self.git_commit).pack(side="left", padx=2)
        ctk.CTkButton(git_btn_frame, text="Push", width=60, height=24, command=self.git_push).pack(side="left", padx=2)
        
        # 3. SNIPPETS (existing...)
        self.snippets_frame = ctk.CTkFrame(self.sidebar_container, fg_color="transparent")
        ctk.CTkLabel(self.snippets_frame, text="CODE SNIPPETS", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=10, pady=5)
        lang_frame = ctk.CTkFrame(self.snippets_frame, fg_color="transparent")
        lang_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(lang_frame, text="Language:", font=("Segoe UI", 10)).pack(side="left", padx=5)
        self.snippet_lang_var = ctk.StringVar(value="python")
        ctk.CTkOptionMenu(lang_frame, values=["python", "javascript", "html", "css"], 
                         variable=self.snippet_lang_var, command=self.refresh_snippets, width=120).pack(side="left", padx=2)
        self.snippet_list = ctk.CTkScrollableFrame(self.snippets_frame, fg_color="transparent")
        self.snippet_list.pack(fill="both", expand=True)
        
        # 4. TASK MANAGER (NEW!)
        self.tasks_frame = ctk.CTkFrame(self.sidebar_container, fg_color="transparent")
        ctk.CTkLabel(self.tasks_frame, text="TASK MANAGER ✅", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=10, pady=5)
        
        task_actions = ctk.CTkFrame(self.tasks_frame, fg_color="transparent")
        task_actions.pack(fill="x", padx=5, pady=5)
        ctk.CTkButton(task_actions, text="➕ Add Task", width=100, height=24, 
                     command=self.add_task_dialog).pack(side="left", padx=2)
        ctk.CTkButton(task_actions, text="Export", width=60, height=24,
                     command=self.export_tasks).pack(side="left", padx=2)
        
        self.task_list = ctk.CTkScrollableFrame(self.tasks_frame, fg_color="transparent")
        self.task_list.pack(fill="both", expand=True)
        
        # Stats
        self.task_stats_label = ctk.CTkLabel(self.tasks_frame, text="Tasks: 0/0", 
                                             font=("Segoe UI", 10), text_color="gray")
        self.task_stats_label.pack(pady=5)
        
        # 5. EXTENSIONS (existing...)
        self.extensions_frame = ctk.CTkFrame(self.sidebar_container, fg_color="transparent")
        ctk.CTkLabel(self.extensions_frame, text="EXTENSIONS", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=10, pady=5)
        self.ext_list = ctk.CTkScrollableFrame(self.extensions_frame, fg_color="transparent")
        self.ext_list.pack(fill="both", expand=True)
        for ext in ["Python", "Pylance", "Jupyter", "Docker", "GitLens", "Prettier"]:
            card = ctk.CTkFrame(self.ext_list, fg_color="#2d2d2d", height=50)
            card.pack(fill="x", pady=2)
            ctk.CTkLabel(card, text=ext, font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=5)
            ctk.CTkButton(card, text="Install", width=60, height=20, fg_color="#0e639c").pack(anchor="e", padx=5, pady=2)

        # Show explorer by default
        self.explorer_frame.pack(fill="both", expand=True)

    def switch_sidebar(self, mode):
        """Switch between sidebar panels"""
        for frame in [self.explorer_frame, self.git_frame, self.snippets_frame, 
                     self.tasks_frame, self.extensions_frame]:
            frame.pack_forget()
        
        if mode == "explorer":
            self.explorer_frame.pack(fill="both", expand=True)
        elif mode == "git":
            self.git_frame.pack(fill="both", expand=True)
            self.git_refresh_status()
        elif mode == "snippets":
            self.snippets_frame.pack(fill="both", expand=True)
            self.refresh_snippets(None)
        elif mode == "tasks":
            self.tasks_frame.pack(fill="both", expand=True)
            self.refresh_task_list()
        elif mode == "extensions":
            self.extensions_frame.pack(fill="both", expand=True)

    def setup_editor(self):
        self.editor_frame = ctk.CTkFrame(self, fg_color=COLORS("bg_main"), corner_radius=0)
        self.editor_frame.grid(row=1, column=2, sticky="nsew")
        self.editor_frame.grid_rowconfigure(1, weight=1)
        self.editor_frame.grid_rowconfigure(2, weight=0, minsize=150)
        self.editor_frame.grid_columnconfigure(0, weight=1)
        
        # Tabs
        self.editor_tabs = ctk.CTkTabview(self.editor_frame, fg_color=COLORS("bg_main"), 
                                          segmented_button_fg_color="#252526", 
                                          segmented_button_selected_color=COLORS("bg_main"))
        self.editor_tabs.grid(row=1, column=0, sticky="nsew")
        
        # Terminal
        self.term_frame = ctk.CTkFrame(self.editor_frame, fg_color=COLORS("bg_main"), 
                                       border_width=1, border_color=COLORS("border"))
        self.term_frame.grid(row=2, column=0, sticky="nsew")
        self.term_frame.grid_rowconfigure(1, weight=1)
        self.term_frame.grid_columnconfigure(0, weight=1)
        
        term_bar = ctk.CTkFrame(self.term_frame, height=25, fg_color=COLORS("bg_activity"))
        term_bar.grid(row=0, column=0, sticky="ew")
        ctk.CTkLabel(term_bar, text="TERMINAL", font=("Segoe UI", 11)).pack(side="left", padx=10)
        
        self.term_out = ctk.CTkTextbox(self.term_frame, font=("Consolas", 12), fg_color=COLORS("bg_main"))
        self.term_out.grid(row=1, column=0, sticky="nsew")
        self.term_out.insert("1.0", "PS C:\\\\Users\\\\Dev> \\n")
        self.term_in = ctk.CTkEntry(self.term_frame, font=("Consolas", 12), fg_color="#3c3c3c", border_width=0)
        self.term_in.grid(row=2, column=0, sticky="ew")
        self.term_in.bind("<Return>", self.exec_terminal)

    def setup_ai_panel(self):
        """Enhanced AI panel with status display"""
        self.ai_frame = ctk.CTkFrame(self, width=350, fg_color=COLORS("bg_sidebar"), corner_radius=0)
        self.ai_frame.grid(row=1, column=3, sticky="nsew")
        self.ai_frame.grid_columnconfigure(0, weight=1)
        self.ai_frame.grid_rowconfigure(1, weight=1)

        # Header with AI STATUS
        header = ctk.CTkFrame(self.ai_frame, height=50, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        ctk.CTkLabel(header, text="AI COPILOT", font=("Segoe UI", 12, "bold")).pack(side="left")
        
        # AI Status Label (Myśli/Szuka/Pisze)
        self.ai_status_lbl = ctk.CTkLabel(header, text="Agent->Gotowy ✅", 
                                         font=("Segoe UI", 10, "italic"), text_color="#4ec9b0")
        self.ai_status_lbl.pack(side="right")

        # Chat area
        self.chat_scroll = ctk.CTkScrollableFrame(self.ai_frame, fg_color=COLORS("bg_main"))
        self.chat_scroll.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        input_frame = ctk.CTkFrame(self.ai_frame, height=100, fg_color="transparent")
        input_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=10)
        
        self.ai_input = ctk.CTkEntry(input_frame, placeholder_text="Ask AI anything...", height=35)
        self.ai_input.pack(fill="x", pady=(0, 5))
        self.ai_input.bind("<Return>", self.send_ai)
        
        ctk.CTkButton(input_frame, text="Generate / Execute", command=self.send_ai, 
                     fg_color="#0e639c").pack(fill="x")
        
        self.chat_append("System", "AI Fervv Enhanced - Ready with status tracking! 🚀")

    def setup_status_bar(self):
        sb = ctk.CTkFrame(self, height=25, fg_color=COLORS("bg_status"), corner_radius=0)
        sb.grid(row=2, column=0, columnspan=4, sticky="ew")
        self.status_lbl = ctk.CTkLabel(sb, text="Ready | Enhanced Edition", text_color="white")
        self.status_lbl.pack(side="left", padx=10)
        
        # Cursor position
        self.cursor_pos_lbl = ctk.CTkLabel(sb, text="Ln 1, Col 1", text_color="white")
        self.cursor_pos_lbl.pack(side="right", padx=10)

    # === AI STATUS CALLBACK ===
    def on_ai_status_change(self, status, details):
        """Called when AI status changes"""
        status_text = status.value[0]
        status_color = status.value[1]
        self.ai_status_lbl.configure(text=status_text, text_color=status_color)
        
        # Log to live logs
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.append_to_log(f"[{ts}] {status_text} {details}\\n")

    # === (Continue in separate file due to length - this demonstrates key features) ===
    
# (Due to character limits, I'll create a separate continuation file with remaining methods)

if __name__ == "__main__":
    print("⚠️ NOTE: This is Part 1 of the complete implementation.")
    print("Full implementation requires additional methods - see main_complete_part2.py")
    print("Core features demonstrated: AI Status, Task Manager, Menus")
    app = FervvIDE()
    app.mainloop()
