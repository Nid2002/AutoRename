# -*- mode: python ; coding: utf-8 -*-

"""
PyInstaller specification for AutoRename.

Defines how standalone executables are generated
for Windows and Linux.

Used both locally and by GitHub Actions.
"""

from pathlib import Path
from PyInstaller.utils.hooks import collect_all

# ==========================================================
# AutoRename v1.0.0
# PyInstaller Specification
# ==========================================================

ICON = "assets/icon.ico"

if not Path(ICON).exists():
    ICON = None

datas = [
    ("config.ini", "."),
]

binaries = []
hiddenimports = []

# ==========================================================
# Pacotes que precisam ser coletados
# ==========================================================

PACOTES = (
    "pdfplumber",
    "pdfminer",
    "PIL",
    "pypdfium2",
)

for pacote in PACOTES:
    d, b, h = collect_all(pacote)

    datas += d
    binaries += b
    hiddenimports += h

# ==========================================================
# Análise
# ==========================================================

a = Analysis(
    ["src/main.py"],
    pathex=["."],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)

# ==========================================================
# Bytecode Python
# ==========================================================

pyz = PYZ(a.pure)

# ==========================================================
# Executável
# ==========================================================

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name="AutoRename",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
    icon=ICON,
)
