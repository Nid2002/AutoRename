# -*- mode: python ; coding: utf-8 -*-

from PyInstaller.utils.hooks import collect_all

datas = [
    ('config.ini', '.'),
]

binaries = []

hiddenimports = []

tmp = collect_all('pdfplumber')
datas += tmp[0]
binaries += tmp[1]
hiddenimports += tmp[2]

tmp = collect_all('pdfminer')
datas += tmp[0]
binaries += tmp[1]
hiddenimports += tmp[2]

tmp = collect_all('PIL')
datas += tmp[0]
binaries += tmp[1]
hiddenimports += tmp[2]

tmp = collect_all('pypdfium2')
datas += tmp[0]
binaries += tmp[1]
hiddenimports += tmp[2]


a = Analysis(
    ['src/main.py'],
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

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='AutoRename',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    icon='icon.ico',
)
