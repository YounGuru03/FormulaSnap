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

# Comprehensive hidden imports for all dependencies
hiddenimports = [
    # PIL/Pillow imports
    'PIL',
    'PIL._tkinter_finder',
    'PIL.Image',
    'PIL.ImageTk',
    'PIL.ImageGrab',
    'PIL.ImageDraw',
    'PIL.ImageFont',
    'PIL.ImageFilter',
    
    # OpenCV imports
    'cv2',
    'cv2.cv2',
    
    # NumPy imports
    'numpy',
    'numpy.core',
    # Note: numpy.core._multiarray_umath is a private module that may change
    # PyInstaller should auto-detect it, but include if you see NumPy import errors
    # 'numpy.core._multiarray_umath',
    
    # PyTorch imports (if using advanced OCR)
    # Uncomment if torch is in requirements.txt
    # 'torch',
    # 'torch.nn',
    # 'torch.optim',
    # 'torchvision',
    # 'torchvision.transforms',
    
    # Transformers (if using)
    # 'transformers',
    # 'transformers.models',
    
    # pix2tex (if using)
    # 'pix2tex',
    # 'pix2tex.cli',
    
    # Clipboard functionality
    'pyperclip',
    
    # Tkinter and GUI
    'tkinter',
    'tkinter.ttk',
    'tkinter.filedialog',
    'tkinter.messagebox',
    'tkinter.scrolledtext',
    '_tkinter',
    
    # Standard library imports that may be missed
    'threading',
    'logging',
    'logging.handlers',
    'tempfile',
    'io',
    'typing',
    'pathlib',
    'argparse',
    'traceback',
    'queue',
    'json',
    'base64',
    'datetime',
    'collections',
    'collections.abc',
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
        # Exclude large unnecessary packages
        'matplotlib',
        'scipy',
        'pandas',
        'jupyter',
        'notebook',
        'IPython',
        'pytest',
        'sphinx',
        'setuptools',
        'pip',
        'wheel',
        'distutils',
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
    'wx',
    'pytest',
    'sphinx',
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
    console=False,  # No console window for GUI application
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon file path here if available (e.g., 'icon.ico')
)