import customtkinter as ctk
from agent import AI_Fervv
import threading
import os
import subprocess
import re
import json
import datetime
from tkinter import filedialog, END, Toplevel, Listbox, Menu
from themes import ThemeManager, THEMES
from snippets import SnippetManager
from git_manager import GitManager
from autocomplete import AutocompleteEngine
from project_templates import TemplateManager
from file_icons import get_file_icon, get_language_from_extension
from ai_status import AIStatusManager, AgentStatus, status_manager
from clipboard_manager import ClipboardManager, UndoRedoManager
from task_manager import TaskManager, TaskPriority, TaskStatus
from panel_manager import PanelManager
from tree_explorer import TreeViewExplorer
from minimap import CodeMinimap

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
        
        # Clear tags
        for tag in ["keyword", "comment", "string", "function", "number"]:
            tb.tag_remove(tag, "1.0", "end")

        if self.lang == "python":
            self.highlight_python(content)
        elif self.lang == "json":
            self.highlight_json(content)
        elif self.lang == "css":
            self.highlight_css(content)

    def highlight_python(self, content):
        # 1. Keywords
        keywords = ["def", "class", "import", "from", "return", "if", "else", "elif", "while", "for", "in", "try", "except", "print", "self", "True", "False", "None", "with", "as", "global", "pass", "break", "continue"]
        pattern_kw = r"\b(" + "|".join(keywords) + r")\b"
        self.apply_tag(pattern_kw, "keyword")
        
        # 2. Functions
        self.apply_tag(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)", "function")
        
        # 3. Strings
        self.apply_tag(r"(\".*?\"|'.*?')", "string")
        
        # 4. Comments
        self.apply_tag(r"(#.*?$)", "comment")
        
        # 5. Numbers
        self.apply_tag(r"\b\d+\b", "number")

    def highlight_json(self, content):
        self.apply_tag(r"(\".*?\")\s*:", "keyword") # Keys
        self.apply_tag(r":\s*(\".*?\")", "string")   # String Values
        self.apply_tag(r"\b\d+\b", "number")         # Numbers
        self.apply_tag(r"\b(true|false|null)\b", "keyword") # Booleans

    def highlight_css(self, content):
        self.apply_tag(r"([a-zA-Z0-9\-_]+)(?=\s*\{)", "function") # Selectors
        self.apply_tag(r"([a-zA-Z0-9\-_]+)(?=:)", "keyword")      # Properties
        self.apply_tag(r":\s*([^;]+);", "string")                 # Values
        self.apply_tag(r"/\*.*?\*/", "comment")                   # Comments

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
        self.grid_columnconfigure(1, weight=1) # Textbox
        self.grid_rowconfigure(0, weight=1)
        
        # 1. Line Numbers Gutter
        self.line_numbers = ctk.CTkTextbox(
            self, width=40, font=("Consolas", font_size),
            fg_color=COLORS("line_num_bg"), text_color=COLORS("line_num_fg"),
            activate_scrollbars=False
        )
        self.line_numbers.grid(row=0, column=0, sticky="ns")
        self.line_numbers.insert("1.0", "1")
        self.line_numbers.configure(state="disabled")
        
        # 2. Main Textbox
        self.textbox = ctk.CTkTextbox(
            self, 
            wrap="none", 
            font=("Consolas", font_size), 
            undo=True,
            fg_color=COLORS("bg_main"),
            text_color=COLORS("fg_text"),
            activate_scrollbars=True
        )
        self.textbox.grid(row=0, column=1, sticky="nsew")
        
        # 3. Sync Scrolling
        # Binding scroll events of underlying widgets
        self.textbox._textbox.configure(yscrollcommand=self.on_text_scroll)
        self.line_numbers._textbox.configure(yscrollcommand=self.on_ln_scroll)

        # 4. Logic
        lang = "python"
        if file_ext.endswith(".json"): lang = "json"
        elif file_ext.endswith(".css"): lang = "css"
        elif file_ext.endswith(".js"): lang = "python" # fallback
        
        self.highlighter = SyntaxHighlighter(self.textbox, lang)
        
        # Bindings
        self.textbox.bind("<KeyRelease>", self.on_key_release)
        self.textbox.bind("<Button-1>", self.on_click)
        self.textbox.bind("<MouseWheel>", self.on_mouse_wheel)

    def on_text_scroll(self, *args):
        self.line_numbers.yview_moveto(args[0])
        # We don't manually set yview of textbox here as it's triggered by scrollbar

    def on_ln_scroll(self, *args):
        self.textbox.yview_moveto(args[0])

    def on_mouse_wheel(self, event):
        # Cross-platform delta handling might be needed, assuming Windows for now
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
            
        # Sync view again just in case
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

# --- MAIN APPLICATION ---
# ... (FervvIDE definition remains same until process_commands)

# Inside FervvIDE class (in separate replace calls or combined if context allows)
# We need to jump to process_commands for the second part.
# Splitting this into two replacements for safety or one if possible. 
# The context view shows lines 1-150. CodeEditor is there. process_commands is at line 428.
# I will do two separate edits. First this one for highlighting.


# --- MAIN APPLICATION ---
class FervvIDE(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # State
        self.current_folder = None
        self.open_documents = {} # path -> tab_name
        self.current_file_path = None
        self.agent = AI_Fervv()
        self.active_sidebar = "explorer" # explorer | extensions | git | snippets | tasks
        self.sidebar_visible = True
        
        # Enhancement Managers
        self.snippet_manager = SnippetManager()
        self.git_manager = GitManager()
        self.template_manager = TemplateManager()
        self.autocomplete_engine = AutocompleteEngine()
        
        # New Advanced Managers
        self.ai_status_manager = status_manager
        self.clipboard_manager = ClipboardManager()
        self.task_manager = TaskManager()
        self.panel_manager = PanelManager()
        self.undo_managers = {}  # Per-file undo/redo

        # UI Config
        self.title("AI Fervv Studio Code - Ultimate Edition 🚀")
        self.geometry("1400x900")
        self.configure(fg_color=COLORS("bg_main"))
        
        # Grid: ActivityBar(0) | Sidebar(1) | Editor(2) | AIProp(3)
        self.grid_columnconfigure(0, weight=0, minsize=50) # Activity
        self.grid_columnconfigure(1, weight=0, minsize=250) # Sidebar
        self.grid_columnconfigure(2, weight=1)              # Editor
        self.grid_columnconfigure(3, weight=0, minsize=350) # AI
        self.grid_rowconfigure(0, weight=0, minsize=30)     # Menu
        self.grid_rowconfigure(1, weight=1)                 # Main
        self.grid_rowconfigure(2, weight=0, minsize=25)     # Status

        self.setup_menu()
        self.setup_activity_bar()
        self.setup_sidebars()
        self.setup_editor()
        self.setup_ai_panel()
        self.setup_status_bar()

        # Keyboard Shortcuts
        self.bind("<Control-s>", self.save_file)
        self.bind("<Control-n>", lambda e: self.create_new_file())
        self.bind("<Control-p>", self.show_command_palette)
        self.bind("<Control-b>", self.toggle_sidebar)
        self.bind("<Control-Shift-p>", self.show_project_templates)
        self.bind("<Control-Shift-t>", self.show_theme_selector)
        self.bind("<Control-Shift-s>", self.show_snippets_quick_insert)
        self.bind("<Control-comma>", self.show_settings)

        # Boot
        self.create_tab("🔴 Live Logs")
        self.set_tab_content("🔴 Live Logs", f"# AGENT SYSTEM LOGS\n# Started at {datetime.datetime.now().strftime('%H:%M:%S')}\n" + "-"*40 + "\n")

        # Load saved settings
        self.load_settings()

        # ANIMATION: Fade In
        self.attributes("-alpha", 0.0)
        self.after(100, self.animate_fade_in)

    def animate_fade_in(self, current_alpha=0.0):
        if current_alpha < 1.0:
            current_alpha += 0.05
            self.attributes("-alpha", current_alpha)
            self.after(20, lambda: self.animate_fade_in(current_alpha))
        else:
            self.attributes("-alpha", 1.0)

    # --- UI COMPONENTS ---
    def setup_menu(self):
        mf = ctk.CTkFrame(self, height=30, fg_color="#303031", corner_radius=0)
        mf.grid(row=0, column=0, columnspan=4, sticky="ew")
        for m in ["File", "Edit", "Selection", "View", "Go", "Run", "Terminal", "Help"]:
            ctk.CTkButton(mf, text=m, fg_color="transparent", width=40, hover_color=COLORS("hover")).pack(side="left", padx=2)
        ctk.CTkLabel(mf, text="AI Fervv Studio", text_color="gray").pack(side="right", padx=10)

    def setup_activity_bar(self):
        f = ctk.CTkFrame(self, width=50, fg_color=COLORS("bg_activity"), corner_radius=0)
        f.grid(row=1, column=0, sticky="nsew")
        
        # Switch buttons
        self.create_activity_btn(f, "📄", "explorer")
        self.create_activity_btn(f, "🔍", "search")
        self.create_activity_btn(f, "🔀", "git")
        self.create_activity_btn(f, "📦", "snippets")
        self.create_activity_btn(f, "🧩", "extensions")
        
        ctk.CTkButton(f, text="⚙", width=40, font=("Arial", 20), fg_color="transparent").pack(side="bottom", pady=10)

    def create_activity_btn(self, parent, icon, mode):
        ctk.CTkButton(
            parent, text=icon, width=40, height=40, 
            fg_color="transparent", font=("Arial", 20), hover_color=COLORS("hover"),
            command=lambda: self.switch_sidebar(mode)
        ).pack(pady=5)

    def setup_sidebars(self):
        self.sidebar_container = ctk.CTkFrame(self, width=250, fg_color=COLORS("bg_sidebar"), corner_radius=0)
        self.sidebar_container.grid(row=1, column=1, sticky="nsew")
        self.sidebar_container.pack_propagate(False) # Force width
        
        # 1. EXPLORER VIEW
        self.explorer_frame = ctk.CTkFrame(self.sidebar_container, fg_color="transparent")
        
        # Header
        h = ctk.CTkFrame(self.explorer_frame, height=30, fg_color="transparent")
        h.pack(fill="x")
        ctk.CTkLabel(h, text="EXPLORER", font=("Segoe UI", 11, "bold")).pack(side="left", padx=10)
        
        # File Action Buttons
        act = ctk.CTkFrame(self.explorer_frame, fg_color="transparent")
        act.pack(fill="x", padx=5, pady=5)
        ctk.CTkButton(act, text="Open Folder", width=110, height=24, command=self.open_folder_dialog).pack(side="left", padx=2)
        ctk.CTkButton(act, text="Refresh", width=60, height=24, command=self.refresh_explorer).pack(side="left", padx=2)

        self.file_list = ctk.CTkScrollableFrame(self.explorer_frame, fg_color="transparent")
        self.file_list.pack(fill="both", expand=True)
        
        # 2. GIT VIEW
        self.git_frame = ctk.CTkFrame(self.sidebar_container, fg_color="transparent")
        ctk.CTkLabel(self.git_frame, text="SOURCE CONTROL", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=10, pady=5)
        
        git_actions = ctk.CTkFrame(self.git_frame, fg_color="transparent")
        git_actions.pack(fill="x", padx=5, pady=5)
        ctk.CTkButton(git_actions, text="Initialize Repo", width=100, height=24, command=self.git_init).pack(side="left", padx=2)
        ctk.CTkButton(git_actions, text="Refresh", width=60, height=24, command=self.git_refresh_status).pack(side="left", padx=2)
        
        self.git_status_list = ctk.CTkScrollableFrame(self.git_frame, fg_color="transparent")
        self.git_status_list.pack(fill="both", expand=True)
        
        git_commit_frame = ctk.CTkFrame(self.git_frame, fg_color="transparent")
        git_commit_frame.pack(fill="x", padx=5, pady=5)
        
        ctk.CTkLabel(git_commit_frame, text="Commit Message:", font=("Segoe UI", 10)).pack(anchor="w")
        self.git_commit_msg = ctk.CTkEntry(git_commit_frame, placeholder_text="Your commit message...")
        self.git_commit_msg.pack(fill="x", pady=2)
        
        git_btn_frame = ctk.CTkFrame(git_commit_frame, fg_color="transparent")
        git_btn_frame.pack(fill="x", pady=2)
        ctk.CTkButton(git_btn_frame, text="Commit", width=70, height=24, command=self.git_commit).pack(side="left", padx=2)
        ctk.CTkButton(git_btn_frame, text="Push", width=60, height=24, command=self.git_push).pack(side="left", padx=2)
        
        # 3. SNIPPETS VIEW
        self.snippets_frame = ctk.CTkFrame(self.sidebar_container, fg_color="transparent")
        ctk.CTkLabel(self.snippets_frame, text="CODE SNIPPETS", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=10, pady=5)
        
        # Language selector
        lang_frame = ctk.CTkFrame(self.snippets_frame, fg_color="transparent")
        lang_frame.pack(fill="x", padx=5, pady=5)
        ctk.CTkLabel(lang_frame, text="Language:", font=("Segoe UI", 10)).pack(side="left", padx=5)
        self.snippet_lang_var = ctk.StringVar(value="python")
        lang_selector = ctk.CTkOptionMenu(lang_frame, values=["python", "javascript", "html", "css"], 
                                          variable=self.snippet_lang_var, command=self.refresh_snippets, width=120)
        lang_selector.pack(side="left", padx=2)
        
        self.snippet_list = ctk.CTkScrollableFrame(self.snippets_frame, fg_color="transparent")
        self.snippet_list.pack(fill="both", expand=True)
        
        # 4. EXTENSIONS VIEW (Existing)
        self.extensions_frame = ctk.CTkFrame(self.sidebar_container, fg_color="transparent")
        ctk.CTkLabel(self.extensions_frame, text="EXTENSIONS", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=10, pady=5)
        self.ext_list = ctk.CTkScrollableFrame(self.extensions_frame, fg_color="transparent")
        self.ext_list.pack(fill="both", expand=True)
        
        # Add dummy extensions
        for ext in ["Python v2024.12", "Pylance", "Jupyter", "Docker", "GitLens", "Prettier"]:
            card = ctk.CTkFrame(self.ext_list, fg_color="#2d2d2d", height=50)
            card.pack(fill="x", pady=2)
            ctk.CTkLabel(card, text=ext, font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=5)
            ctk.CTkButton(card, text="Install", width=60, height=20, fg_color="#0e639c").pack(anchor="e", padx=5, pady=2)

        # Default Show Explorer
        self.explorer_frame.pack(fill="both", expand=True)

    def switch_sidebar(self, mode):
        self.explorer_frame.pack_forget()
        self.extensions_frame.pack_forget()
        self.git_frame.pack_forget()
        self.snippets_frame.pack_forget()
        
        if mode == "explorer":
            self.explorer_frame.pack(fill="both", expand=True)
        elif mode == "git":
            self.git_frame.pack(fill="both", expand=True)
            self.git_refresh_status()  # Auto-refresh on open
        elif mode == "snippets":
            self.snippets_frame.pack(fill="both", expand=True)
            self.refresh_snippets(None)  # Load snippets
        elif mode == "extensions":
            self.extensions_frame.pack(fill="both", expand=True)
        elif mode == "search":
            # TODO: Implement search panel
            pass

    def setup_editor(self):
        self.editor_frame = ctk.CTkFrame(self, fg_color=COLORS("bg_main"), corner_radius=0)
        self.editor_frame.grid(row=1, column=2, sticky="nsew")
        self.editor_frame.grid_rowconfigure(1, weight=1) # Editor
        self.editor_frame.grid_rowconfigure(2, weight=0, minsize=150) # Terminal
        self.editor_frame.grid_columnconfigure(0, weight=1)
        
        # Tabs
        self.editor_tabs = ctk.CTkTabview(self.editor_frame, fg_color=COLORS("bg_main"), 
                                          segmented_button_fg_color="#252526", segmented_button_selected_color=COLORS("bg_main"))
        self.editor_tabs.grid(row=1, column=0, sticky="nsew")
        
        # Terminal
        self.term_frame = ctk.CTkFrame(self.editor_frame, fg_color=COLORS("bg_main"), border_width=1, border_color=COLORS("border"))
        self.term_frame.grid(row=2, column=0, sticky="nsew")
        self.term_frame.grid_rowconfigure(1, weight=1)
        self.term_frame.grid_columnconfigure(0, weight=1)
        
        term_bar = ctk.CTkFrame(self.term_frame, height=25, fg_color=COLORS("bg_activity"))
        term_bar.grid(row=0, column=0, sticky="ew")
        ctk.CTkLabel(term_bar, text="TERMINAL", font=("Segoe UI", 11)).pack(side="left", padx=10)
        
        self.term_out = ctk.CTkTextbox(self.term_frame, font=("Consolas", 12), fg_color=COLORS("bg_main"))
        self.term_out.grid(row=1, column=0, sticky="nsew")
        self.term_out.insert("1.0", "PS C:\\Users\\Dev> \n")
        self.term_in = ctk.CTkEntry(self.term_frame, font=("Consolas", 12), fg_color="#3c3c3c", border_width=0)
        self.term_in.grid(row=2, column=0, sticky="ew")
        self.term_in.bind("<Return>", self.exec_terminal)

    def setup_ai_panel(self):
        self.ai_frame = ctk.CTkFrame(self, width=350, fg_color=COLORS("bg_sidebar"), corner_radius=0)
        self.ai_frame.grid(row=1, column=3, sticky="nsew")
        self.ai_frame.grid_columnconfigure(0, weight=1)
        self.ai_frame.grid_rowconfigure(1, weight=1)

        # Header with Status
        header = ctk.CTkFrame(self.ai_frame, height=40, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        ctk.CTkLabel(header, text="AI COPILOT", font=("Segoe UI", 12, "bold")).pack(side="left")
        
        self.ai_status_lbl = ctk.CTkLabel(header, text="Ready", font=("Segoe UI", 10, "italic"), text_color="gray")
        self.ai_status_lbl.pack(side="right") # Status indicator

        # CHAT SCROLL AREA
        self.chat_scroll = ctk.CTkScrollableFrame(self.ai_frame, fg_color=COLORS("bg_main"))
        self.chat_scroll.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        input_frame = ctk.CTkFrame(self.ai_frame, height=100, fg_color="transparent")
        input_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=10)
        
        self.ai_input = ctk.CTkEntry(input_frame, placeholder_text="Ask Agent to Create/Edit/Run...", height=35)
        self.ai_input.pack(fill="x", pady=(0, 5))
        self.ai_input.bind("<Return>", self.send_ai)
        
        ctk.CTkButton(input_frame, text="Generate / Execute", command=self.send_ai, fg_color="#0e639c").pack(fill="x")
        
        # Initial Message
        self.chat_append("System", "Ready. Code blocks will be hidden by default.")

    def append_to_log(self, text):
        # Find the logs tab
        if "🔴 Live Logs" in self.editor_tabs._tab_dict:
            tab = self.editor_tabs.tab("🔴 Live Logs")
            for child in tab.winfo_children():
                if isinstance(child, CodeEditor):
                    child.append_text(text)
                    break
        
    def set_ai_status(self, text):
        self.ai_status_lbl.configure(text=text)
        if "Thinking" in text or "Processing" in text:
            self.ai_status_lbl.configure(text_color="#007acc") # Blue for active
        elif "Error" in text:
            self.ai_status_lbl.configure(text_color="red")
        else:
            self.ai_status_lbl.configure(text_color="gray")
            
        # LIVE LOG
        try:
            ts = datetime.datetime.now().strftime("%H:%M:%S")
            self.append_to_log(f"[{ts}] {text}\n")
        except: pass

    def setup_status_bar(self):
        sb = ctk.CTkFrame(self, height=25, fg_color=COLORS("bg_status"), corner_radius=0)
        sb.grid(row=2, column=0, columnspan=4, sticky="ew")
        self.status_lbl = ctk.CTkLabel(sb, text="Ready", text_color="white")
        self.status_lbl.pack(side="left", padx=10)

    # --- ACTION LOGIC ---
    def open_folder_dialog(self):
        p = filedialog.askdirectory()
        if p:
            self.current_folder = p
            self.refresh_explorer()
            self.status_lbl.configure(text=f"Workspace: {p}")

    def refresh_explorer(self):
        if not self.current_folder: return
        for w in self.file_list.winfo_children(): w.destroy()
        
        try:
            items = sorted(os.listdir(self.current_folder), key=lambda x: (os.path.isfile(os.path.join(self.current_folder, x)), x.lower()))
            for item in items:
                path = os.path.join(self.current_folder, item)
                is_file = os.path.isfile(path)
                
                # Icon Logic - Use new system
                icon = get_file_icon(item, is_directory=not is_file)
                
                # Careful with lambda scope!
                cmd = None
                if is_file:
                    cmd = lambda p=path: self.open_file(p)
                
                btn = ctk.CTkButton(
                    self.file_list, text=f"{icon} {item}", anchor="w", 
                    fg_color="transparent", text_color="#cccccc", hover_color=COLORS("hover"),
                    height=24,
                    command=cmd
                )
                btn.pack(fill="x")
        except Exception as e:
            print(e)
            
    def open_file(self, path):
        fname = os.path.basename(path)
        # 1. Existing tab?
        if path in self.open_documents:
            self.editor_tabs.set(self.open_documents[path])
            self.current_file_path = path
            return
        
        # 2. Open new
        try:
            with open(path, "r", encoding="utf-8") as f: content = f.read()
            self.create_tab(fname, path)
            self.set_tab_content(fname, content)
            self.open_documents[path] = fname
            self.current_file_path = path
            self.status_lbl.configure(text=f"Editing {fname}")
        except Exception as e:
            self.chat_append("System", f"Error opening file: {e}")

    def create_tab(self, name, path=None):
        try: self.editor_tabs.add(name)
        except: pass
        self.editor_tabs.set(name)
        
        ext = os.path.splitext(name)[1] if "." in name else ".py"
        editor = CodeEditor(self.editor_tabs.tab(name), file_ext=ext)
        editor.pack(fill="both", expand=True)
        return editor

    def set_tab_content(self, unique_name, content):
        tab = self.editor_tabs.tab(unique_name)
        for child in tab.winfo_children():
            if isinstance(child, CodeEditor):
                child.set_text(content)
                break

    def get_editor_content(self, unique_name=None):
        if not unique_name: unique_name = self.editor_tabs.get()
        tab = self.editor_tabs.tab(unique_name)
        for child in tab.winfo_children():
            if isinstance(child, CodeEditor):
                return child.get_text()
        return ""

    def save_file(self, event=None):
        if not self.current_file_path: return
        try:
            content = self.get_editor_content()
            with open(self.current_file_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.status_lbl.configure(text=f"Saved {os.path.basename(self.current_file_path)}")
        except Exception as e:
            self.chat_append("System", f"Save Error: {e}")

    def create_new_file(self):
        # Placeholder for Ctrl+N
        self.chat_append("System", "Use AI to create files (e.g. 'Create test.py')")

    def animate_text(self, label, full_text, idx=0):
        if idx < len(full_text):
            label.configure(text=full_text[:idx+1])
            # Scroll down occasionally
            if idx % 50 == 0: self.chat_scroll._parent_canvas.yview_moveto(1.0)
            self.after(5, lambda: self.animate_text(label, full_text, idx+1)) # 5ms per char
        else:
             self.chat_scroll._parent_canvas.yview_moveto(1.0)
    def send_ai(self, event=None):
        txt = self.ai_input.get()
        if not txt: return
        self.ai_input.delete(0, "end")
        self.chat_append("You", txt)
        
        # STATUS: Thinking
        self.set_ai_status("Thinking... 🧠")
        
        # Context building
        ctx = ""
        
        # 1. Project Structure
        if self.current_folder:
            structure = self.get_project_structure()
            ctx += f"\n[PROJECT STRUCTURE (Root: {self.current_folder})]:\n```\n{structure}\n```\n"

        # 2. Editor Context
        if self.current_file_path:
             content = self.get_editor_content()
             if len(content) > 3000: content = content[:3000] + "...(truncated)"
             ctx += f"\n[ACTIVE FILE: {os.path.basename(self.current_file_path)}]\n```\n{content}\n```\n"
        
        # 3. Terminal Context
        try:
            term_history = self.term_out.get("end-2000c", "end")
            ctx += f"\n[TERMINAL OUTPUT HISTORY]:\n```\n{term_history}\n```\n"
        except: pass
        
        # 4. Agent Instructions
        ctx += "\n[SYSTEM]: You have access to the file structure above. If asked to build/run something, check the file list first."
        ctx += "\n[SYSTEM]: If the user asks to execute a plan, READ it and output [[CREATE]]/[[EXEC]] commands."

        threading.Thread(target=self.ai_worker, args=(ctx + txt,), daemon=True).start()

    def get_project_structure(self):
        """Generates a simple tree view of files (depth 2)"""
        if not self.current_folder: return "(No folder open)"
        tree = ""
        try:
            for root, dirs, files in os.walk(self.current_folder):
                level = root.replace(self.current_folder, '').count(os.sep)
                if level > 2: continue # Limit depth
                indent = ' ' * 4 * level
                tree += f"{indent}{os.path.basename(root)}/\n"
                subindent = ' ' * 4 * (level + 1)
                for f in files:
                    tree += f"{subindent}{f}\n"
        except Exception as e:
            tree = f"Error listing files: {e}"
        return tree

    def ai_worker(self, prompt):
        resp = self.agent.generate_response(prompt)
        
        # STATUS: Parsing
        self.after(0, lambda: self.set_ai_status("Processing Response... 📋"))
        
        self.after(0, lambda: self.chat_append("AI", resp))
        self.after(0, lambda: self.process_commands(resp))

    def chat_append(self, role, msg):
        # Create Message Bubble
        bubble = ctk.CTkFrame(self.chat_scroll, fg_color="#2b2b2b" if role == "AI" else "#37373d")
        bubble.pack(fill="x", pady=5, padx=5)
        
        # Header
        ctk.CTkLabel(bubble, text=f"[{role}]", font=("Segoe UI", 10, "bold"), text_color="gray").pack(anchor="w", padx=5)
        
        parts = re.split(r"(```.*?```)", msg, flags=re.DOTALL)
        
        for part in parts:
            if part.startswith("```"):
                # CODE BLOCK (No animation for performance)
                code_content = part.strip("`").strip()
                if not code_content: continue
                
                btn = ctk.CTkButton(bubble, text="▶ Show/Hide Code", height=20, fg_color="#444", width=100)
                btn.pack(anchor="w", padx=5, pady=2)
                
                code_box = ctk.CTkTextbox(bubble, height=0, font=("Consolas", 11), fg_color="#1e1e1e", text_color="#d4d4d4")
                code_box.insert("1.0", code_content)
                code_box.configure(state="disabled")
                
                def toggle(b=btn, box=code_box, h=100):
                    if box.winfo_height() < 5:
                        box.pack(fill="x", padx=5, pady=2)
                        box.configure(height=h)
                        b.configure(fg_color="#0e639c")
                    else:
                        box.pack_forget()
                        box.configure(height=0)
                        b.configure(fg_color="#444")
                btn.configure(command=toggle)
                
            else:
                # TEXT (Typewriter Animation if AI)
                if not part.strip(): continue
                lbl = ctk.CTkLabel(bubble, text="", wraplength=300, justify="left", anchor="w")
                lbl.pack(anchor="w", padx=5)
                
                if role == "AI":
                    self.animate_text(lbl, part)
                else:
                    lbl.configure(text=part) # Instant for User

        self.after(100, lambda: self.chat_scroll._parent_canvas.yview_moveto(1.0))

    def process_commands(self, text):
        # 1. CREATE
        cp = re.compile(r"\[\[CREATE:(.*?)\]\](.*?)\[\[/CREATE\]\]", re.DOTALL)
        for fname, content in cp.findall(text):
            fname = fname.strip()
            content = content.strip()
            
            # STATUS: Creating
            self.set_ai_status(f"Creating {os.path.basename(fname)}... 🔨")
            self.update_idletasks()
            
            if self.current_folder:
                fpath = os.path.join(self.current_folder, fname)
            else:
                fpath = os.path.abspath(fname)
                
            try:
                # 1. Ensure dir exists
                os.makedirs(os.path.dirname(fpath), exist_ok=True)
                
                # 2. Write content
                with open(fpath, "w", encoding="utf-8") as f: f.write(content)
                self.after(0, lambda: self.chat_append("System", f"Created {fname}"))

                # 3. AUTO-WORKSPACE
                if self.current_folder is None:
                    self.current_folder = os.path.dirname(fpath)
                    self.after(0, lambda: self.status_lbl.configure(text=f"Workspace: {self.current_folder}"))

                # 4. Refresh Live
                self.after(50, self.refresh_explorer)
                
                # 5. AUTO OPEN
                if fpath in self.open_documents:
                    tab_name = self.open_documents[fpath]
                    self.after(100, lambda t=tab_name, c=content: self.set_tab_content(t, c))
                else:
                    self.after(100, lambda p=fpath: self.open_file(p))
                    
            except Exception as e:
                    self.after(0, lambda: self.chat_append("Error", str(e)))

        # 2. DELETE
        dp = re.compile(r"\[\[DELETE:(.*?)\]\]")
        for fname in dp.findall(text):
            fname = fname.strip()
            
            # STATUS: Deleting
            self.set_ai_status(f"Deleting {fname}... 🗑️")
            self.update_idletasks()
            
            if self.current_folder:
                fpath = os.path.join(self.current_folder, fname)
                try: 
                    os.remove(fpath)
                    self.after(0, lambda: self.chat_append("System", f"Deleted {fname}"))
                    self.after(0, self.refresh_explorer)
                except Exception as e:
                    self.after(0, lambda: self.chat_append("Error", str(e)))

        # 3. EXEC
        ep = re.compile(r"\[\[EXEC:(.*?)\]\]")
        for cmd in ep.findall(text):
             # STATUS: Executing
            self.set_ai_status(f"Running Command... ⚡")
            self.update_idletasks()
            self.after(0, lambda c=cmd.strip(): self.exec_terminal(cmd=c))

        # STATUS: Done
        self.after(1000, lambda: self.set_ai_status("Ready"))

    def exec_terminal(self, event=None, cmd=None):
        if not cmd:
            cmd = self.term_in.get()
            self.term_in.delete(0, "end")
        
        if not cmd: return
        
        self.term_out.insert("end", f"\n> {cmd}\n")
        
        def _th():
            try:
                r = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=self.current_folder or ".")
                out = r.stdout + r.stderr
                self.after(0, lambda: self.term_out.insert("end", out))
                self.after(0, lambda: self.term_out.see("end"))
            except Exception as e:
                self.after(0, lambda: self.term_out.insert("end", f"Err: {e}\n"))
        
        threading.Thread(target=_th, daemon=True).start()

    def create_new_file(self):
        # Trigger AI to create file or just simple dialog
        # For professional feel, let's just focus AI input
        self.ai_input.focus_set()
        self.chat_append("System", "Type 'Create [filename]' to generate a new file.")

    def toggle_sidebar(self, event=None):
        if self.sidebar_visible:
            self.sidebar_container.grid_remove()
            self.sidebar_visible = False
        else:
            self.sidebar_container.grid()
            self.sidebar_visible = True

    def show_command_palette(self, event=None):
        # Overlay Frame
        self.cmd_overlay = ctk.CTkFrame(self, fg_color="#2b2b2b", border_width=1, border_color="#007acc")
        self.cmd_overlay.place(relx=0.5, rely=0.1, anchor="n", width=500, height=300)
        
        # Input
        self.cmd_entry = ctk.CTkEntry(self.cmd_overlay, placeholder_text="> Type a command...", font=("Segoe UI", 12))
        self.cmd_entry.pack(fill="x", padx=5, pady=5)
        self.cmd_entry.bind("<Escape>", lambda e: self.cmd_overlay.destroy())
        self.cmd_entry.bind("<Return>", self.exec_command_palette)
        self.cmd_entry.focus_set()
        
        # List
        self.cmd_list = ctk.CTkScrollableFrame(self.cmd_overlay, fg_color="transparent")
        self.cmd_list.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Commands to show
        commands = [
            ("File: Save", self.save_file),
            ("File: New", self.create_new_file),
            ("View: Toggle Sidebar", self.toggle_sidebar),
            ("View: Toggle Fullscreen", lambda: self.attributes("-fullscreen", not self.attributes("-fullscreen"))),
            ("AI: Generate Code", lambda: self.ai_input.focus_set() or self.cmd_overlay.destroy()),
            ("Editor: Clear Logs", lambda: self.set_tab_content("🔴 Live Logs", "# Logs Cleared\n")),
        ]
        
        for name, func in commands:
            btn = ctk.CTkButton(
                self.cmd_list, text=name, anchor="w", 
                fg_color="transparent", hover_color="#37373d", 
                command=lambda f=func: (f(), self.cmd_overlay.destroy())
            )
            btn.pack(fill="x")

    def exec_command_palette(self, event):
        # Basic: just destroy, meant for clicking buttons
        self.cmd_overlay.destroy()

    def show_find_overlay(self, event=None):
        self.find_overlay = ctk.CTkFrame(self, fg_color="#2b2b2b", border_width=1, border_color="#007acc")
        self.find_overlay.place(relx=0.95, rely=0.1, anchor="ne", width=300, height=50)
        
        self.find_entry = ctk.CTkEntry(self.find_overlay, placeholder_text="Find...", width=180)
        self.find_entry.pack(side="left", padx=5, pady=5)
        self.find_entry.bind("<Return>", self.find_next)
        self.find_entry.focus_set()
        
        ctk.CTkButton(self.find_overlay, text="⬇", width=30, command=self.find_next).pack(side="left", padx=2)
        ctk.CTkButton(self.find_overlay, text="X", width=30, fg_color="#c42b1c", command=lambda: self.find_overlay.destroy()).pack(side="left", padx=5)

    def find_next(self, event=None):
        query = self.find_entry.get()
        if not query: return
        
        # Get active editor
        tab = self.editor_tabs.get()
        editor = None
        for child in self.editor_tabs.tab(tab).winfo_children():
            if isinstance(child, CodeEditor): 
                editor = child
                break
        
        if editor:
            text_widget = editor.textbox._textbox
            # Simple find: start from current insert position
            pos = text_widget.search(query, "insert", stopindex="end", nocase=True)
            if not pos:
                # Wrap around
                pos = text_widget.search(query, "1.0", stopindex="end", nocase=True)
            
            if pos:
                # Select it
                end_pos = f"{pos}+{len(query)}c"
                text_widget.tag_remove("sel", "1.0", "end")
                text_widget.tag_add("sel", pos, end_pos)
                text_widget.mark_set("insert", end_pos)
                text_widget.see(pos)

    def load_settings(self):
        try:
            if os.path.exists("settings.json"):
                with open("settings.json", "r") as f:
                    data = json.load(f)
                    if "geometry" in data and data["geometry"]: 
                        try:
                            self.geometry(data["geometry"])
                        except:
                            pass  # Invalid geometry, skip
                    if "folder" in data and data["folder"] and os.path.exists(data["folder"]):
                        self.current_folder = data["folder"]
                        self.git_manager.set_repo_path(self.current_folder)
                        self.status_lbl.configure(text=f"Workspace: {self.current_folder}")
                        self.refresh_explorer()
                    if "theme" in data and data["theme"]:
                        theme_manager.set_theme(data["theme"])
        except Exception as e:
            print(f"Settings error: {e}")

    def save_settings(self):
        data = {
            "geometry": self.geometry(),
            "folder": self.current_folder,
            "theme": theme_manager.current_theme
        }
        try:
            with open("settings.json", "w") as f:
                json.dump(data, f)
        except: pass
    
    # === TASK MANAGER METHODS ===
    def add_task_dialog(self):
        dialog = Toplevel(self)
        dialog.title("Add Task")
        dialog.geometry("400x350")
        dialog.configure(bg=COLORS("bg_main"))
        ctk.CTkLabel(dialog, text="Task Title:", font=("Segoe UI", 12)).pack(pady=5, padx=10, anchor="w")
        title_entry = ctk.CTkEntry(dialog, width=350)
        title_entry.pack(pady=5, padx=10)
        ctk.CTkLabel(dialog, text="Description:", font=("Segoe UI", 12)).pack(pady=5, padx=10, anchor="w")
        desc_text = ctk.CTkTextbox(dialog, width=350, height=100)
        desc_text.pack(pady=5, padx=10)
        ctk.CTkLabel(dialog, text="Priority:", font=("Segoe UI", 12)).pack(pady=5, padx=10, anchor="w")
        priority_var = ctk.StringVar(value="MEDIUM")
        ctk.CTkOptionMenu(dialog, values=["LOW", "MEDIUM", "HIGH"], variable=priority_var).pack(pady=5, padx=10)
        ctk.CTkLabel(dialog, text="Tags:", font=("Segoe UI", 12)).pack(pady=5, padx=10, anchor="w")
        tags_entry = ctk.CTkEntry(dialog, width=350)
        tags_entry.pack(pady=5, padx=10)
        def create_task():
            title = title_entry.get()
            if not title: return
            desc = desc_text.get("1.0", "end-1c")
            priority = TaskPriority[priority_var.get()]
            tags = [t.strip() for t in tags_entry.get().split(",") if t.strip()]
            self.task_manager.add_task(title, desc, priority, tags=tags)
            self.refresh_task_list()
            dialog.destroy()
            self.chat_append("System", f"Task created: {title}")
        ctk.CTkButton(dialog, text="Create Task", command=create_task).pack(pady=10)
    
    def refresh_task_list(self):
        for w in self.task_list.winfo_children(): w.destroy()
        tasks = self.task_manager.tasks
        if not tasks:
            ctk.CTkLabel(self.task_list, text="No tasks", text_color="gray").pack(pady=20)
            return
        for task in tasks:
            card = ctk.CTkFrame(self.task_list, fg_color="#2d2d2d")
            card.pack(fill="x", pady=2, padx=5)
            check_var = ctk.BooleanVar(value=(task.status == TaskStatus.DONE))
            check = ctk.CTkCheckBox(card, text="", variable=check_var,
                                   command=lambda t=task, v=check_var: self.toggle_task_status(t, v))
            check.pack(side="left", padx=5)
            title_color = "#888" if task.status == TaskStatus.DONE else "#fff"
            ctk.CTkLabel(card, text=task.title, font=("Segoe UI", 11), text_color=title_color).pack(side="left", padx=5)
            priority_colors = {"LOW": "#4ec9b0", "MEDIUM": "#dcdcaa", "HIGH": "#f48771"}
            ctk.CTkLabel(card, text="●", text_color=priority_colors[task.priority.name]).pack(side="right", padx=5)
        stats = self.task_manager.get_statistics()
        self.task_stats_label.configure(text=f"Tasks: {stats['done']}/{stats['total']} ({stats['completion_rate']:.0f}%)")
    
    def toggle_task_status(self, task, check_var):
        if check_var.get(): task.mark_done()
        else: task.mark_todo()
        self.task_manager.save_tasks()
        self.refresh_task_list()
    
    def export_tasks(self):
        md = self.task_manager.export_to_markdown()
        path = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown", "*.md")])
        if path:
            with open(path, 'w') as f: f.write(md)
            self.chat_append("System", f"Exported to {path}")
    
    # === CLIPBOARD OPERATIONS ===
    def cut(self, event=None):
        tab = self.editor_tabs.get()
        for child in self.editor_tabs.tab(tab).winfo_children():
            if isinstance(child, CodeEditor):
                try:
                    text = child.textbox._textbox.selection_get()
                    if text:
                        self.clipboard_manager.cut(text)
                        child.textbox._textbox.delete("sel.first", "sel.last")
                        self.save_undo_state(child)
                        self.status_lbl.configure(text="Cut")
                except: pass
        return "break"
    
    def copy(self, event=None):
        tab = self.editor_tabs.get()
        for child in self.editor_tabs.tab(tab).winfo_children():
            if isinstance(child, CodeEditor):
                try:
                    text = child.textbox._textbox.selection_get()
                    if text:
                        self.clipboard_manager.copy(text)
                        self.status_lbl.configure(text="Copied")
                except: pass
        return "break"
    
    def paste(self, event=None):
        tab = self.editor_tabs.get()
        for child in self.editor_tabs.tab(tab).winfo_children():
            if isinstance(child, CodeEditor):
                text = self.clipboard_manager.paste()
                if text:
                    child.textbox.insert("insert", text)
                    self.save_undo_state(child)
                    self.status_lbl.configure(text="Pasted")
        return "break"
    
    def undo(self, event=None):
        tab = self.editor_tabs.get()
        if tab not in self.undo_managers:
            self.undo_managers[tab] = UndoRedoManager()
        manager = self.undo_managers[tab]
        state = manager.undo()
        if state is not None:
            for child in self.editor_tabs.tab(tab).winfo_children():
                if isinstance(child, CodeEditor):
                    child.set_text(state)
                    self.status_lbl.configure(text="Undo")
        return "break"
    
    def redo(self, event=None):
        tab = self.editor_tabs.get()
        if tab not in self.undo_managers: return "break"
        manager = self.undo_managers[tab]
        state = manager.redo()
        if state is not None:
            for child in self.editor_tabs.tab(tab).winfo_children():
                if isinstance(child, CodeEditor):
                    child.set_text(state)
                    self.status_lbl.configure(text="Redo")
        return "break"
    
    def save_undo_state(self, editor):
        tab = self.editor_tabs.get()
        if tab not in self.undo_managers:
            self.undo_managers[tab] = UndoRedoManager()
        state = editor.get_text()
        self.undo_managers[tab].save_state(state)
    
    def select_all(self, event=None):
        tab = self.editor_tabs.get()
        for child in self.editor_tabs.tab(tab).winfo_children():
            if isinstance(child, CodeEditor):
                child.textbox._textbox.tag_add("sel", "1.0", "end")
                self.status_lbl.configure(text="All selected")
        return "break"
    
    # === MENU IMPLEMENTATIONS ===
    def new_file(self):
        count = len([t for t in self.editor_tabs._tab_dict.keys() if "Untitled" in t])
        name = f"Untitled-{count+1}.py"
        self.create_tab(name)
        self.chat_append("System", f"Created {name}")
    
    def open_file_dialog(self):
        path = filedialog.askopenfilename()
        if path: self.open_file(path)
    
    def save_as(self):
        path = filedialog.asksaveasfilename(defaultextension=".py")
        if path:
            self.current_file_path = path
            self.save_file()
    
    def close_current_tab(self):
        tab = self.editor_tabs.get()
        if tab and tab != "🔴 Live Logs":
            self.editor_tabs.delete(tab)
            if tab in self.open_documents: del self.open_documents[tab]
    
    def show_find_dialog(self, event=None):
        self.show_find_overlay()
    
    def go_to_line(self):
        from tkinter import simpledialog
        line = simpledialog.askinteger("Go to Line", "Line number:")
        if line:
            tab = self.editor_tabs.get()
            for child in self.editor_tabs.tab(tab).winfo_children():
                if isinstance(child, CodeEditor):
                    child.textbox._textbox.mark_set("insert", f"{line}.0")
                    child.textbox.see(f"{line}.0")
    
    def toggle_terminal(self):
        if self.term_frame.winfo_viewable(): self.term_frame.grid_remove()
        else: self.term_frame.grid()
    
    def toggle_ai_panel(self):
        if self.ai_frame.winfo_viewable(): self.ai_frame.grid_remove()
        else: self.ai_frame.grid()
    
    def clear_terminal(self):
        self.term_out.delete("1.0", "end")
        self.term_out.insert("1.0", "PS C:\\\\> \\n")
    
    def run_with_python(self):
        self.run_file()
    
    def show_shortcuts(self):
        from tkinter import messagebox
        messagebox.showinfo("Shortcuts", "Ctrl+N: New | Ctrl+S: Save | Ctrl+Z: Undo | Ctrl+Y: Redo\\nCtrl+X: Cut | Ctrl+C: Copy | Ctrl+V: Paste | F5 Run")
    
    def show_about(self):
        from tkinter import messagebox
        messagebox.showinfo("About", "AI Fervv IDE Complete Enhanced Edition\\nVersion 3.0")
        
    # === ENHANCED METHODS ===
    def on_ai_status_change(self, status, details):
        status_text = status.value[0]
        status_color = status.value[1]
        self.ai_status_lbl.configure(text=status_text, text_color=status_color)
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.append_to_log(f"[{ts}] {status_text}\\n")
    
    # === GIT METHODS ===
    def git_init(self):
        if not self.current_folder:
            self.chat_append("System", "Please open a folder first")
            return
        
        self.git_manager.set_repo_path(self.current_folder)
        result = self.git_manager.init_repo()
        
        if result["success"]:
            self.chat_append("Git", "Repository initialized successfully")
            self.git_refresh_status()
        else:
            self.chat_append("Git Error", result["error"])
    
    def git_refresh_status(self):
        if not self.current_folder:
            return
       
        self.git_manager.set_repo_path(self.current_folder)
        
        if not self.git_manager.is_git_repo():
            for w in self.git_status_list.winfo_children(): w.destroy()
            ctk.CTkLabel(self.git_status_list, text="Not a Git repository", text_color="gray").pack(pady=10)
            return
        
        status = self.git_manager.get_status()
        if not status:
            return
        
        # Clear list
        for w in self.git_status_list.winfo_children(): w.destroy()
        
        # Show current branch
        branch = self.git_manager.get_current_branch()
        if branch:
            ctk.CTkLabel(self.git_status_list, text=f"Branch: {branch}", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=5, pady=2)
        
        # Modified files
        if status["modified"]:
            ctk.CTkLabel(self.git_status_list, text="Modified:", font=("Segoe UI", 10, "bold"), text_color="#e2c08d").pack(anchor="w", padx=5)
            for f in status["modified"]:
                ctk.CTkLabel(self.git_status_list, text=f"  • {f}", text_color="#e2c08d").pack(anchor="w", padx=10)
        
        # Untracked files
        if status["untracked"]:
            ctk.CTkLabel(self.git_status_list, text="Untracked:", font=("Segoe UI", 10, "bold"), text_color="#73c991").pack(anchor="w", padx=5)
            for f in status["untracked"]:
                ctk.CTkLabel(self.git_status_list, text=f"  • {f}", text_color="#73c991").pack(anchor="w", padx=10)
        
        # Staged files
        if status["staged"]:
            ctk.CTkLabel(self.git_status_list, text="Staged:", font=("Segoe UI", 10, "bold"), text_color="#4ec9b0").pack(anchor="w", padx=5)
            for f in status["staged"]:
                ctk.CTkLabel(self.git_status_list, text=f"  • {f}", text_color="#4ec9b0").pack(anchor="w", padx=10)
        
        if not status["modified"] and not status["untracked"] and not status["staged"]:
            ctk.CTkLabel(self.git_status_list, text="No changes", text_color="gray").pack(pady=10)
    
    def git_commit(self):
        msg = self.git_commit_msg.get()
        if not msg:
            self.chat_append("Git", "Please enter a commit message")
            return
        
        self.git_manager.set_repo_path(self.current_folder)
        
        # Stage all changes
        self.git_manager.add_all()
        
        # Commit
        result = self.git_manager.commit(msg)
        
        if result["success"]:
            self.chat_append("Git", f"Committed: {msg}")
            self.git_commit_msg.delete(0, "end")
            self.git_refresh_status()
        else:
            self.chat_append("Git Error", result["error"])
    
    def git_push(self):
        self.git_manager.set_repo_path(self.current_folder)
        self.chat_append("Git", "Pushing to remote...")
        
        def push_thread():
            result = self.git_manager.push()
            if result["success"]:
                self.after(0, lambda: self.chat_append("Git", "Pushed successfully"))
            else:
                self.after(0, lambda: self.chat_append("Git Error", result["error"]))
        
        threading.Thread(target=push_thread, daemon=True).start()
    
    # === SNIPPETS METHODS ===
    def refresh_snippets(self, event=None):
        lang = self.snippet_lang_var.get()
        snippets = self.snippet_manager.get_snippets_for_language(lang)
        
        # Clear list
        for w in self.snippet_list.winfo_children(): w.destroy()
        
        if not snippets:
            ctk.CTkLabel(self.snippet_list, text="No snippets available", text_color="gray").pack(pady=10)
            return
        
        # Display snippets
        for snip_id, snip_data in snippets.items():
            card = ctk.CTkFrame(self.snippet_list, fg_color="#2d2d2d")
            card.pack(fill="x", pady=2, padx=5)
            
            ctk.CTkLabel(card, text=snip_data["name"], font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=5)
            ctk.CTkLabel(card, text=snip_data["description"], font=("Segoe UI", 9), text_color="gray").pack(anchor="w", padx=5)
            
            ctk.CTkButton(
                card, text="Insert", width=60, height=20, fg_color="#0e639c",
                command=lambda c=snip_data["code"]: self.insert_snippet(c)
            ).pack(anchor="e", padx=5, pady=2)
    
    def insert_snippet(self, code):
        # Insert into active editor
        tab = self.editor_tabs.get()
        for child in self.editor_tabs.tab(tab).winfo_children():
            if isinstance(child, CodeEditor):
                child.textbox.insert("insert", code)
                child.highlighter.highlight()
                child.update_line_numbers()
                break
        
        self.chat_append("System", "Snippet inserted")
    
    def show_snippets_quick_insert(self, event=None):
        # Quick snippet insert dialog
        dialog = Toplevel(self)
        dialog.title("Quick Snippet Insert")
        dialog.geometry("400x300")
        dialog.configure(bg=COLORS("bg_main"))
        
        ctk.CTkLabel(dialog, text="Select Snippet", font=("Segoe UI", 14, "bold")).pack(pady=10)
        
        search_entry = ctk.CTkEntry(dialog, placeholder_text="Search snippets...")
        search_entry.pack(fill="x", padx=10, pady=5)
        
        listbox_frame = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        listbox_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Populate with all snippets from all languages
        for lang in ["python", "javascript", "html", "css"]:
            snippets = self.snippet_manager.get_snippets_for_language(lang)
            for snip_id, snip_data in snippets.items():
                btn = ctk.CTkButton(
                    listbox_frame,
                    text=f"{snip_data['name']} ({lang})",
                    anchor="w",
                    command=lambda c=snip_data["code"]: (self.insert_snippet(c), dialog.destroy())
                )
                btn.pack(fill="x", pady=2)
    
    # === THEME METHODS ===
    def show_theme_selector(self, event=None):
        dialog = Toplevel(self)
        dialog.title("Theme Selector")
        dialog.geometry("350x400")
        dialog.configure(bg=COLORS("bg_main"))
        
        ctk.CTkLabel(dialog, text="Select Theme", font=("Segoe UI", 14, "bold")).pack(pady=10)
        
        theme_list = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        theme_list.pack(fill="both", expand=True, padx=10, pady=5)
        
        for theme_name in theme_manager.get_all_themes():
            btn = ctk.CTkButton(
                theme_list,
                text=theme_name,
                anchor="w",
                width=280,
                height=40,
                command=lambda t=theme_name: self.apply_theme(t, dialog)
            )
            btn.pack(fill="x", pady=2)
    
    def apply_theme(self, theme_name, dialog=None):
        theme_manager.set_theme(theme_name)
        self.chat_append("System", f"Theme changed to: {theme_name}")
        self.chat_append("System", "Please restart the application for full effect")
        if dialog:
            dialog.destroy()
    
    # === PROJECT TEMPLATES ===
    def show_project_templates(self, event=None):
        dialog = Toplevel(self)
        dialog.title("Create Project from Template")
        dialog.geometry("500x400")
        dialog.configure(bg=COLORS("bg_main"))
        
        ctk.CTkLabel(dialog, text="Project Templates", font=("Segoe UI", 14, "bold")).pack(pady=10)
        
        template_list = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        template_list.pack(fill="both", expand=True, padx=10, pady=5)
        
        templates = self.template_manager.get_all_templates()
        
        for template_key, template_info in templates.items():
            card = ctk.CTkFrame(template_list, fg_color="#2d2d2d")
            card.pack(fill="x", pady=5, padx=5)
            
            ctk.CTkLabel(card, text=template_info["name"], font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=10, pady=2)
            ctk.CTkLabel(card, text=template_info["description"], font=("Segoe UI", 10), text_color="gray").pack(anchor="w", padx=10)
            
            ctk.CTkButton(
                card, text="Create Project", width=120, height=24, fg_color="#0e639c",
                command=lambda k=template_key: self.create_from_template(k, dialog)
            ).pack(anchor="e", padx=10, pady=5)
    
    def create_from_template(self, template_key, dialog):
        folder = filedialog.askdirectory(title="Select destination folder")
        if not folder:
            return
        
        success, message = self.template_manager.create_project(template_key, folder)
        
        if success:
            self.chat_append("System", message)
            self.current_folder = folder
            self.refresh_explorer()
            dialog.destroy()
        else:
            self.chat_append("Error", message)
    
    # === SETTINGS PANEL ===
    def show_settings(self, event=None):
        dialog = Toplevel(self)
        dialog.title("Settings")
        dialog.geometry("600x500")
        dialog.configure(bg=COLORS("bg_main"))
        
        ctk.CTkLabel(dialog, text="⚙ Settings", font=("Segoe UI", 16, "bold")).pack(pady=15)
        
        settings_frame = ctk.CTkScrollableFrame(dialog)
        settings_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Theme Setting
        theme_section = ctk.CTkFrame(settings_frame, fg_color="#2d2d2d")
        theme_section.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(theme_section, text="Theme", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=10, pady=5)
        
        theme_var = ctk.StringVar(value=theme_manager.current_theme)
        theme_menu = ctk.CTkOptionMenu(
            theme_section,
            values=theme_manager.get_all_themes(),
            variable=theme_var,
            command=lambda t: theme_manager.set_theme(t)
        )
        theme_menu.pack(fill="x", padx=10, pady=5)
        
        # Font Size (TODO: Implement)
        font_section = ctk.CTkFrame(settings_frame, fg_color="#2d2d2d")
        font_section.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(font_section, text="Editor Font Size", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=10, pady=5)
        font_slider = ctk.CTkSlider(font_section, from_=10, to=24)
        font_slider.set(14)
        font_slider.pack(fill="x", padx=10, pady=5)
        
        # About
        about_section = ctk.CTkFrame(settings_frame, fg_color="#2d2d2d")
        about_section.pack(fill="x", pady=10, padx=10)
        
        ctk.CTkLabel(about_section, text="About", font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=10, pady=5)
        ctk.CTkLabel(about_section, text="AI Fervv Studio Code - Ultimate Edition", text_color="gray").pack(anchor="w", padx=10)
        ctk.CTkLabel(about_section, text="Version 2.0 with AI Enhancement", text_color="gray").pack(anchor="w", padx=10)
        
        # Close button
        ctk.CTkButton(dialog, text="Close", width=100, command=dialog.destroy).pack(pady=10)
        
    def destroy(self):
        self.save_settings()
        super().destroy()

if __name__ == "__main__":
    app = FervvIDE()
    app.mainloop()