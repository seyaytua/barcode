# -*- mode: python ; coding: utf-8 -*-

import sys
from pathlib import Path

block_cipher = None

a = Analysis(
    ['main_v2.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'PySide6.QtCore',
        'PySide6.QtGui',
        'PySide6.QtWidgets',
        'barcode.writer',
        'qrcode.image.pil',
        'qrcode.image.svg',
        'PIL._tkinter_finder',
        'reportlab.pdfgen',
        'reportlab.lib',
        'reportlab.pdfbase',
        'reportlab.pdfbase.cidfonts',
        'PyPDF2',
        'openpyxl',
        'openpyxl.styles',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
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
    name='BarcodeQRCodePDF_v2',
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
    version='version_info_v2.txt',
)

# macOS bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        exe,
        name='BarcodeQRCodePDF_v2.app',
        icon=None,
        bundle_identifier='com.barcode.qrcode.pdf.v2',
        info_plist={
            'NSHighResolutionCapable': 'True',
            'CFBundleShortVersionString': '2.0.0',
            'CFBundleVersion': '2.0.0',
        },
    )
