"""
AI Fervv IDE - Integrated Web Browser
Built-in browser for documentation, live preview, and web development
"""

import customtkinter as ctk
from tkinter import Frame
import tkinter as tk

class WebBrowser(ctk.CTkFrame):
    """Integrated web browser panel"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color="#1e1e1e", **kwargs)
        
        self.current_url = "about:blank"
        
        # Browser toolbar
        self.setup_toolbar()
        
        # Browser content (using tkinterweb or placeholder)
        self.setup_browser()
    
    def setup_toolbar(self):
        """Create browser toolbar"""
        toolbar = ctk.CTkFrame(self, height=40, fg_color="#2d2d2d")
        toolbar.pack(fill="x", padx=5, pady=5)
        
        # Navigation buttons
        btn_frame = ctk.CTkFrame(toolbar, fg_color="transparent")
        btn_frame.pack(side="left", padx=5)
        
        ctk.CTkButton(btn_frame, text="◀", width=30, command=self.go_back).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="▶", width=30, command=self.go_forward).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="⟳", width=30, command=self.refresh).pack(side="left", padx=2)
        ctk.CTkButton(btn_frame, text="⌂", width=30, command=self.go_home).pack(side="left", padx=2)
        
        # URL bar
        self.url_entry = ctk.CTkEntry(toolbar, placeholder_text="Enter URL...")
        self.url_entry.pack(side="left", fill="x", expand=True, padx=10)
        self.url_entry.bind("<Return>", lambda e: self.navigate(self.url_entry.get()))
        
        # Go button
        ctk.CTkButton(toolbar, text="Go", width=50, command=lambda: self.navigate(self.url_entry.get())).pack(side="left", padx=5)
    
    def setup_browser(self):
        """Setup browser content area"""
        # Try to use tkinterweb if available, otherwise use Text widget as placeholder
        try:
            import tkinterweb
            self.browser_frame = Frame(self, bg="#ffffff")
            self.browser_frame.pack(fill="both", expand=True, padx=5, pady=5)
            
            self.browser = tkinterweb.HtmlFrame(self.browser_frame)
            self.browser.pack(fill="both", expand=True)
            
            self.has_browser = True
        except ImportError:
            # Fallback: use Text widget
            self.browser_frame = ctk.CTkFrame(self, fg_color="#ffffff")
            self.browser_frame.pack(fill="both", expand=True, padx=5, pady=5)
            
            info = ctk.CTkTextbox(self.browser_frame, fg_color="#ffffff", text_color="#000000")
            info.pack(fill="both", expand=True)
            info.insert("1.0", "Browser Preview\n\n" +
                       "To enable full web browsing, install: pip install tkinterweb\n\n" +
                       "For now, you can:\n" +
                       "- Preview HTML files\n" +
                       "- Access documentation\n" +
                       "- Use external browser\n\n" +
                       "Enter URL above and press Go to open in external browser.")
            
            self.browser = info
            self.has_browser = False
    
    def navigate(self, url):
        """Navigate to URL"""
        if not url:
            return
        
        # Add https:// if no protocol
        if not url.startswith(('http://', 'https://', 'file://', 'about:')):
            url = 'https://' + url
        
        self.current_url = url
        self.url_entry.delete(0, "end")
        self.url_entry.insert(0, url)
        
        if self.has_browser:
            try:
                self.browser.load_url(url)
            except:
                pass
        else:
            # Open in external browser
            import webbrowser
            webbrowser.open(url)
    
    def load_html(self, html_content):
        """Load HTML content directly"""
        if self.has_browser:
            try:
                self.browser.load_html(html_content)
            except:
                pass
    
    def load_file(self, file_path):
        """Load local HTML file"""
        import os
        if os.path.exists(file_path):
            url = f"file:///{os.path.abspath(file_path)}"
            self.navigate(url)
    
    def go_back(self):
        """Go back in history"""
        if self.has_browser and hasattr(self.browser, 'go_back'):
            self.browser.go_back()
    
    def go_forward(self):
        """Go forward in history"""
        if self.has_browser and hasattr(self.browser, 'go_forward'):
            self.browser.go_forward()
    
    def refresh(self):
        """Refresh current page"""
        if self.current_url:
            self.navigate(self.current_url)
    
    def go_home(self):
        """Go to home page"""
        self.navigate("https://www.google.com")

class LivePreview(ctk.CTkFrame):
    """Live HTML/CSS/JS preview"""
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.browser = WebBrowser(self)
        self.browser.pack(fill="both", expand=True)
        
        self.auto_update = True
    
    def update_preview(self, html_content):
        """Update preview with HTML content"""
        if self.auto_update:
            self.browser.load_html(html_content)
    
    def toggle_auto_update(self):
        """Toggle auto-update"""
        self.auto_update = not self.auto_update
