# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['customtkinter', 'tkinter', 'PIL', 'openai', 'google.generativeai', 'src', 'src.core', 'src.core.container', 'src.core.event_bus', 'src.services', 'src.services.ai_service', 'src.services.config_service', 'src.services.theme_service', 'src.ui', 'src.ui.workbench', 'src.ui.workbench.workbench', 'src.ui.editor', 'src.ui.editor.code_editor', 'src.ui.editor.syntax_highlighter', 'src.languages', 'src.languages.language_registry'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tensorflow', 'numpy', 'pandas', 'matplotlib', 'scipy', 'sklearn', 'torch', 'cv2'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AI_Fervv_IDE',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
