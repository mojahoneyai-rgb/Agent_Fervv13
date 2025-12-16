"""
Automatic Integration Script
Applies all enhancements to main.py
"""

import re
import shutil
from datetime import datetime

def patch_main():
    print("🚀 AI Fervv IDE - Automatic Integration")
    print("=" * 50)
    
    # Backup
    backup_name = f"main_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
    shutil.copy("main.py", backup_name)
    print(f"✅ Backup created: {backup_name}")
    
    with open("main.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # 1. Add imports
    print("📦 Adding imports...")
    import_section = """from tree_explorer import TreeViewExplorer
from minimap import CodeMinimap
from plugin_system import PluginManager
from web_browser import WebBrowser, LivePreview
"""
    
    if "from tree_explorer import" not in content:
        content = content.replace(
            "from panel_manager import PanelManager",
            "from panel_manager import PanelManager\n" + import_section
        )
    
    # 2. Initialize managers
    print("⚙️ Initializing managers...")
    content = content.replace(
        "self.undo_managers = {}  # Per-file undo/redo",
        """self.undo_managers = {}  # Per-file undo/redo
        self.plugin_manager = PluginManager(self)
        self.web_browser = None"""
    )
    
    # 3. Replace file_list with TreeView
    print("🌳 Installing TreeView explorer...")
    content = re.sub(
        r'self\.file_list = ctk\.CTkScrollableFrame\(self\.explorer_frame.*?\)\s*self\.file_list\.pack\(fill="both", expand=True\)',
        '''self.file_tree = TreeViewExplorer(self.explorer_frame, on_file_click=self.open_file)
        self.file_tree.pack(fill="both", expand=True)''',
        content,
        flags=re.DOTALL
    )
    
    # 4. Update refresh_explorer
    print("🔄 Updating refresh_explorer...")
    refresh_pattern = r'def refresh_explorer\(self\):.*?except.*?pass'
    new_refresh = '''def refresh_explorer(self):
        """Refresh file tree"""
        if self.current_folder and hasattr(self, 'file_tree'):
            self.file_tree.load_folder(self.current_folder)
        # Fallback for old style
        elif self.current_folder and hasattr(self, 'file_list'):
            for widget in self.file_list.winfo_children():
                widget.destroy()
            try:
                items = os.listdir(self.current_folder)
                dirs = [d for d in items if os.path.isdir(os.path.join(self.current_folder, d))]
                files = [f for f in items if os.path.isfile(os.path.join(self.current_folder, f))]
                dirs.sort()
                files.sort()
                for d in dirs:
                    path = os.path.join(self.current_folder, d)
                    icon = get_file_icon(d, is_directory=True)
                    btn = ctk.CTkButton(self.file_list, text=f"{icon} {d}", anchor="w", fg_color="transparent")
                    btn.pack(fill="x", pady=1)
                for f in files:
                    path = os.path.join(self.current_folder, f)
                    icon = get_file_icon(f)
                    btn = ctk.CTkButton(self.file_list, text=f"{icon} {f}", anchor="w", fg_color="transparent", command=lambda p=path: self.open_file(p))
                    btn.pack(fill="x", pady=1)
            except: pass'''
    
    content = re.sub(refresh_pattern, new_refresh, content, flags=re.DOTALL)
    
    # 5. Add browser to activity bar
    print("🌐 Adding browser to activity bar...")
    content = content.replace(
        'self.create_activity_btn(f, "🧩", "extensions")',
        '''self.create_activity_btn(f, "🧩", "extensions")
        self.create_activity_btn(f, "🌐", "browser")'''
    )
    
    # 6. Add browser frame in sidebars (find extensions_frame and add after)
    print("📱 Adding browser sidebar...")
    browser_frame_code = '''
        # 6. BROWSER
        self.browser_frame = ctk.CTkFrame(self.sidebar_container, fg_color="transparent")
        ctk.CTkLabel(self.browser_frame, text="WEB BROWSER 🌐", font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=10, pady=5)
        
        browser_actions = ctk.CTkFrame(self.browser_frame, fg_color="transparent")
        browser_actions.pack(fill="x", padx=5, pady=5)
        ctk.CTkButton(browser_actions, text="Open Browser", width=120, height=24, command=self.open_browser_panel).pack(side="left", padx=2)
        ctk.CTkButton(browser_actions, text="Live Preview", width=100, height=24, command=self.open_live_preview).pack(side="left", padx=2)
        
        self.browser_container = ctk.CTkFrame(self.browser_frame, fg_color="#1e1e1e")
        self.browser_container.pack(fill="both", expand=True, pady=5)
'''
    
    # Find where extensions frame setup ends
    ext_pattern = r'(self\.ext_list\.pack\(fill="both", expand=True\).*?for ext in.*?pass\n)'
    content = re.sub(ext_pattern, r'\1' + browser_frame_code, content, flags=re.DOTALL)
    
    # 7. Update switch_sidebar
    print("🔀 Updating switch_sidebar...")
    content = content.replace(
        'for frame in [self.explorer_frame, self.git_frame, self.snippets_frame, \n                     self.tasks_frame, self.extensions_frame]:',
        'for frame in [self.explorer_frame, self.git_frame, self.snippets_frame, \n                     self.tasks_frame, self.extensions_frame, self.browser_frame]:'
    )
    
    content = content.replace(
        'elif mode == "extensions":\n            self.extensions_frame.pack(fill="both", expand=True)',
        '''elif mode == "extensions":
            self.extensions_frame.pack(fill="both", expand=True)
        elif mode == "browser":
            self.browser_frame.pack(fill="both", expand=True)'''
    )
    
    # 8. Add browser methods before destroy
    print("🔧 Adding browser methods...")
    browser_methods = '''
    def open_browser_panel(self):
        """Open web browser"""
        if not self.web_browser:
            self.web_browser = WebBrowser(self.browser_container)
            self.web_browser.pack(fill="both", expand=True)
        self.web_browser.navigate("https://www.google.com")
        self.chat_append("System", "Browser opened")
    
    def open_live_preview(self):
        """Open live HTML preview"""
        tab = self.editor_tabs.get()
        if tab and (tab.endswith('.html') or tab.endswith('.htm')):
            for child in self.editor_tabs.tab(tab).winfo_children():
                if isinstance(child, CodeEditor):
                    html_content = child.get_text()
                    if not self.web_browser:
                        self.open_browser_panel()
                    self.web_browser.load_html(html_content)
                    self.chat_append("System", "Live preview loaded")
                    break
        else:
            self.chat_append("System", "Open an HTML file first")
    
    def load_plugins(self):
        """Load plugins"""
        plugins = self.plugin_manager.discover_plugins()
        for plugin in plugins:
            if self.plugin_manager.load_plugin(plugin):
                self.chat_append("System", f"Loaded: {plugin['name']}")
'''
    
    content = content.replace(
        '    def destroy(self):',
        browser_methods + '\n    def destroy(self):'
    )
    
    # 9. Remove Live Logs creation
    print("🗑️ Removing Live Logs...")
    content = re.sub(
        r'# Boot\s*self\.create_tab\("🔴 Live Logs"\).*?self\.set_tab_content.*?\n',
        '# Boot - Clean start\n        pass\n',
        content,
        flags=re.DOTALL
    )
    
    # 10. Add minimap to title
    print("📝 Updating title...")
    content = content.replace(
        'AI Fervv Studio Code - Complete Enhanced Edition',
        'AI Fervv Studio Code - Ultimate Edition Pro'
    )
    
    # Write updated content
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(content)
    
    print("\n✅ All patches applied successfully!")
    print(f"📄 Original backed up to: {backup_name}")
    print("🎯 Ready to run!")
    
    return True

if __name__ == "__main__":
    try:
        patch_main()
        print("\n" + "="*50)
        print("🎉 Integration Complete!")
        print("Run: python main.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Check backup file if needed")
