# -*- mode: python ; coding: utf-8 -*-

import sys
import os

# Asegurar que PyInstaller encuentre los módulos
block_cipher = None

a = Analysis(
    ['src/main.py'],
    pathex=[os.path.abspath(SPECPATH)],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PIL',
        'PIL._imagingtk',
        'PIL._tkinter_finder',
        'src.icon_generator',
        'src.config_manager',
        'src.preview_manager',
        'src.flutter_integration',
        'json',
        'dataclasses',
        'yaml',
        'subprocess',
        'shutil',
        'pathlib',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'PyQt5',
        'PyQt6',
        'PySide2',
        'PySide6',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FlutterIconGenerator',
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
    icon='assets/icon.ico' if os.path.exists('assets/icon.ico') else None,
)
