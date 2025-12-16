"""
AI Fervv IDE - Elite Edition
Bootstrap script.
"""
import customtkinter as ctk
import os
import sys

# Ensure src is in path
sys.path.append(os.path.dirname(__file__))

from src.core.kernel.kernel import kernel
from src.core.vfs.vfs import VirtualFileSystem
from src.services.config_service import ConfigService
from src.services.theme_service import ThemeService
from src.services.ai_service import AIService
from src.ui.workbench.workbench import Workbench

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # 0. Global Settings
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        
        # 1. Bootstrap Kernel
        self._init_kernel()
        
        # 2. Setup Window
        self.title("AI Fervv IDE - Galactic Edition")
        self.geometry("1400x900")
        
        # 3. Apply Theme
        # Adapting legacy services to Kernel
        theme_svc = kernel.get_service("ThemeService") 
        if theme_svc:
            self.configure(fg_color=theme_svc.get_color("bg_main"))
        
        # 4. Launch Workbench
        self.workbench = Workbench(self)
        self.workbench.pack(fill="both", expand=True)

    def _init_kernel(self):
        # 1. Bootstrap Logger
        from src.services.logger_service import setup_logger
        self.logger = setup_logger(kernel)
        kernel.log("🚀 Bootstrapping Galactic Kernel...")
        
        # 2. Bridge Container EARLY to support service inter-dependencies
        from src.core.container import Container
        Container._instances = kernel.services 
        
        # 3. Load VFS Extension
        vfs = VirtualFileSystem()
        vfs.on_load(kernel)
        
        # 4. Register Legacy Services
        config = ConfigService()
        kernel.register_service("ConfigService", config)
        
        theme = ThemeService()
        kernel.register_service("ThemeService", theme)

        from src.services.file_service import FileService
        file_svc = FileService()
        # kernel.register_service("FileService", file_svc) # Kernel registration
        # But Container adapter takes kernel.services.
        kernel.register_service("FileService", file_svc)
        
        ai = AIService()
        ai.initialize()
        kernel.register_service("AIService", ai)
        
        # Events
        from src.core.event_bus import global_event_bus
        global_event_bus.subscribe("open_settings", lambda _: self.show_settings())
        
        kernel.log("✅ Kernel Ready.")

    def show_settings(self):
        # Placeholder for existing settings logic or new implementation
        # Assuming the method exists or creating a simple one
        top = ctk.CTkToplevel(self)
        top.title("Settings")
        top.geometry("400x300")
        ctk.CTkLabel(top, text="Settings (Galactic Edition)", font=("Segoe UI", 16, "bold")).pack(pady=20)
        ctk.CTkLabel(top, text="Theme Configured via Service.", text_color="gray").pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()