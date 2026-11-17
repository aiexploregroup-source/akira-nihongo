# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller recipe for AKIRA NIHONGO (single-file Windows executable)."""

from PyInstaller.utils.hooks import collect_submodules

block_cipher = None

# Keep the resource layout identical to the source tree so Path(__file__)-based
# font and logo loading keeps working inside the one-file bundle.
datas = [
    ("nihongo_app/resources/fonts/InterVariable.ttf", "nihongo_app/resources/fonts"),
    ("nihongo_app/resources/fonts/NotoSansJP-Variable.ttf", "nihongo_app/resources/fonts"),
    ("nihongo_app/resources/akira_logo.svg", "nihongo_app/resources"),
    ("nihongo_app/resources/akira_logo.png", "nihongo_app/resources"),
]

hiddenimports = collect_submodules("nihongo_app") + [
    "PySide6.QtTextToSpeech",
]

a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=["tkinter", "matplotlib", "numpy", "PIL"],
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
    name="AkiraNihongo",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="nihongo_app/resources/akira_logo.ico",
)
