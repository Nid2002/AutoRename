# -*- mode: python ; coding: utf-8 -*-

from pathlib import Path
from PyInstaller.utils.hooks import collect_all

# ==========================================================
# Configurações
# ==========================================================

ICON = "icon.ico" if Path("icon.ico").exists() else None

datas = [
    ("config.ini", "."),
]

binaries = []
hiddenimports = []

# ==========================================================
# Bibliotecas que precisam ser coletadas
# ==========================================================

for pacote in (
    "pdfplumber",
    "pdfminer",
    "PIL",
    "pypdfium2",
):

    tmp = collect_all(pacote)

    datas += tmp[0]
    binaries += tmp[1]
    hiddenimports += tmp[2]

# ==========================================================
# Análise
# ==========================================================

a = Analysis(
    ["src/main.py"],
    pathex=[],
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
# Python bytecode
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
    upx=True,
    console=True,
    icon=ICON,
)
