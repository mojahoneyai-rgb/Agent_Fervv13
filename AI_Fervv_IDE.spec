# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = []
binaries = []
hiddenimports = ['customtkinter', 'tkinter', 'PIL', 'openai', 'google.generativeai', 'duckduckgo_search', 'src', 'src.core', 'src.core.container', 'src.core.event_bus', 'src.services', 'src.services.ai_service', 'src.services.memory_service', 'src.services.config_service', 'src.services.theme_service', 'src.ui', 'src.ui.workbench', 'src.ui.workbench.workbench', 'src.ui.editor', 'src.ui.editor.code_editor', 'src.ui.editor.syntax_highlighter', 'src.languages', 'src.languages.language_registry']
tmp_ret = collect_all('customtkinter')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('duckduckgo_search')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tensorflow', 'numpy', 'pandas', 'scipy', 'sklearn', 'torch', 'cv2'],
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
