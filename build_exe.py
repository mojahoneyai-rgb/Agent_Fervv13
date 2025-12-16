"""
Build script for AI Fervv IDE
Tworzy executable używając PyInstaller z właściwą konfiguracją
"""

import os
import subprocess
import sys

print("=" * 60)
print("AI Fervv IDE - Build Script")
print("=" * 60)

# Ensure we're in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Build command with all necessary options
build_cmd = [
    sys.executable,
    "-m", "PyInstaller",
    "--clean",
    "--onefile",
    "--noconsole",
    "--name", "AI_Fervv_IDE",
    # Hidden imports for new architecture
    "--hidden-import", "customtkinter",
    "--hidden-import", "tkinter",
    "--hidden-import", "PIL",
    "--hidden-import", "openai",
    "--hidden-import", "google.generativeai",
    # Src modules
    "--hidden-import", "src",
    "--hidden-import", "src.core",
    "--hidden-import", "src.core.container",
    "--hidden-import", "src.core.event_bus",
    "--hidden-import", "src.services",
    "--hidden-import", "src.services.ai_service",
    "--hidden-import", "src.services.config_service",
    "--hidden-import", "src.services.theme_service",
    "--hidden-import", "src.ui",
    "--hidden-import", "src.ui.workbench",
    "--hidden-import", "src.ui.workbench.workbench",
    "--hidden-import", "src.ui.editor",
    "--hidden-import", "src.ui.editor.code_editor",
    "--hidden-import", "src.ui.editor.syntax_highlighter",
    "--hidden-import", "src.languages",
    "--hidden-import", "src.languages.language_registry",
    # Exclude heavy modules
    "--exclude-module", "tensorflow",
    "--exclude-module", "numpy",
    "--exclude-module", "pandas",
    "--exclude-module", "matplotlib",
    "--exclude-module", "scipy",
    "--exclude-module", "sklearn",
    "--exclude-module", "torch",
    "--exclude-module", "cv2",
    # Main file
    "main.py"
]

print("\nBuilding executable...")
print("This may take a few minutes...")
print()

try:
    result = subprocess.run(build_cmd, check=True)
    print("\n" + "=" * 60)
    print("✅ BUILD SUCCESSFUL!")
    print("=" * 60)
    print(f"\nExecutable location: dist\\AI_Fervv_IDE.exe")
    print("\nYou can now run the application by double-clicking the .exe file")
except subprocess.CalledProcessError as e:
    print("\n" + "=" * 60)
    print("❌ BUILD FAILED")
    print("=" * 60)
    print(f"\nError code: {e.returncode}")
    print("\nTrying alternative build method...")
    
    # Alternative: onedir instead of onefile
    print("\nBuilding with --onedir option (faster, multiple files)...")
    
    build_cmd_alt = [
        sys.executable,
        "-m", "PyInstaller",
        "--clean",
        "--onedir",  # Changed from onefile
        "--noconsole",
        "--name", "AI_Fervv_IDE",
        "--hidden-import", "customtkinter",
        "--hidden-import", "tkinter",
        "--hidden-import", "PIL",
        "--hidden-import", "openai",
        "--hidden-import", "google.generativeai",
        # Src modules
        "--hidden-import", "src",
        "--hidden-import", "src.core",
        "--hidden-import", "src.core.container",
        "--hidden-import", "src.core.event_bus",
        "--hidden-import", "src.services",
        "--hidden-import", "src.services.ai_service",
        "--hidden-import", "src.services.config_service",
        "--hidden-import", "src.services.logger_service",
        "--hidden-import", "src.services.theme_service",
        "--hidden-import", "src.services.file_service",
        "--hidden-import", "src.core.kernel",
        "--hidden-import", "src.core.kernel.kernel",
        "--hidden-import", "src.core.vfs",
        "--hidden-import", "src.core.vfs.vfs",
        "--hidden-import", "src.core.interfaces",
        "--hidden-import", "src.core.interfaces.extension",
        "--hidden-import", "src.agent_os",
        "--hidden-import", "src.agent_os.tools",
        "--hidden-import", "src.agent_os.autonomous_agent",
        "--hidden-import", "src.languages.lsp",
        "--hidden-import", "src.languages.lsp.client",
        "--hidden-import", "src.languages.lsp.manager",
        "--hidden-import", "src.ui",
        "--hidden-import", "src.ui.workbench",
        "--hidden-import", "src.ui.workbench.workbench",
        "--hidden-import", "src.ui.docking",
        "--hidden-import", "src.ui.docking.dock_manager",
        "--hidden-import", "src.ui.widgets",
        "--hidden-import", "src.ui.widgets.terminal",
        "--hidden-import", "src.ui.editor",
        "--hidden-import", "src.ui.editor",
        "--hidden-import", "src.ui.editor.code_editor",
        "--hidden-import", "src.ui.editor.syntax_highlighter",
        "--hidden-import", "src.ui.views",
        "--hidden-import", "src.ui.views.explorer",
        "--hidden-import", "src.ui.views.chat_view",
        "--hidden-import", "src.ui.views.git_view",
        "--hidden-import", "src.ui.views.snippets_view",
        "--hidden-import", "src.ui.views.tasks_view",
        "--hidden-import", "src.languages",
        "--hidden-import", "src.languages.language_registry",
        "main.py"
    ]
    
    try:
        subprocess.run(build_cmd_alt, check=True)
        print("\n" + "=" * 60)
        print("✅ ALTERNATIVE BUILD SUCCESSFUL!")
        print("=" * 60)
        print(f"\nExecutable location: dist\\AI_Fervv_IDE\\AI_Fervv_IDE.exe")
        print("\nNote: This creates a folder with the exe and supporting files")
    except subprocess.CalledProcessError:
        print("\n❌ Both build methods failed")
        print("\nPlease check the error messages above")
        sys.exit(1)
