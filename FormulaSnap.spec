# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from pathlib import Path

# Add source directory to path
sys.path.insert(0, os.path.abspath('.'))

block_cipher = None

# Define data files and hidden imports
datas = [
    # Add any data files here if needed
]

hiddenimports = [
    'PIL',
    'PIL._tkinter_finder',
    'cv2',
    'numpy',
    'torch',
    'torchvision',
    'transformers',
    'pix2tex',
    'pyperclip',
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.scrolledtext',
    'threading',
    'logging',
    'tempfile',
    'io',
    'typing',
]

# Analysis
a = Analysis(
    ['formulasnap/main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'scipy',
        'pandas',
        'jupyter',
        'notebook',
        'IPython',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# Remove unnecessary packages to reduce size
excluded_modules = [
    'matplotlib',
    'scipy',
    'pandas',
    'jupyter',
    'notebook',
    'IPython',
    'zmq',
    'PyQt5',
    'PyQt6',
    'PySide2',
    'PySide6',
]

a.binaries = [x for x in a.binaries if not any(excluded in x[0] for excluded in excluded_modules)]
a.datas = [x for x in a.datas if not any(excluded in x[0] for excluded in excluded_modules)]

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='FormulaSnap',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon file path here if available
)