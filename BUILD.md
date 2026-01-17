# FormulaSnap Build Guide

This guide provides detailed instructions for building and testing FormulaSnap locally.

## Prerequisites

### Required Software
- **Windows 10/11** (64-bit) - Required for building Windows executables
- **Python 3.10** - Recommended version (3.8-3.11 also supported)
- **Git** - For version control
- **Visual C++ Redistributable** - Usually pre-installed on Windows 10/11

### System Requirements
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 2GB free space for build environment
- **CPU**: Any modern x64 processor

## Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/YounGuru03/FormulaSnap.git
cd FormulaSnap
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows Command Prompt:
venv\Scripts\activate.bat

# On Windows PowerShell:
venv\Scripts\Activate.ps1

# On Git Bash:
source venv/Scripts/activate
```

### 3. Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# Install project dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

### 4. Test the Application (Development Mode)

```bash
# Run the application directly
python -m formulasnap.main

# Run with debug logging
python -m formulasnap.main --debug

# Check version
python -m formulasnap.main --version
```

## Building the Executable

### Method 1: Using Build Script (Recommended)

```bash
# Run the automated build script
python scripts/build_exe.py
```

This script will:
- Clean previous builds
- Install PyInstaller if needed
- Build the executable using the spec file
- Verify the build
- Report the executable size

### Method 2: Manual PyInstaller Build

```bash
# Install PyInstaller
pip install pyinstaller>=6.0.0

# Clean previous builds (optional)
rmdir /s /q build dist
del FormulaSnap.spec.bak

# Build using spec file
pyinstaller --clean --noconfirm FormulaSnap.spec

# The executable will be at: dist\FormulaSnap.exe
```

### Method 3: Direct PyInstaller Command

If you don't have a spec file or want to customize:

```bash
pyinstaller --name=FormulaSnap ^
  --onefile ^
  --windowed ^
  --icon=icon.ico ^
  --add-data "formulasnap;formulasnap" ^
  --hidden-import=PIL ^
  --hidden-import=cv2 ^
  --hidden-import=numpy ^
  --hidden-import=tkinter ^
  formulasnap/main.py
```

## Testing the Built Executable

### Basic Functionality Tests

```bash
# Test version command
dist\FormulaSnap.exe --version

# Test help command
dist\FormulaSnap.exe --help

# Run the application
dist\FormulaSnap.exe
```

### Manual Testing Checklist

- [ ] **Startup**: Application launches without errors
- [ ] **UI**: All UI elements are visible and properly rendered
- [ ] **Clipboard Paste**: Ctrl+V successfully pastes images
- [ ] **File Open**: Can browse and open image files
- [ ] **Image Processing**: Extract formula button works
- [ ] **Results Display**: LaTeX and Typst tabs show results
- [ ] **Copy Functions**: Copy buttons work correctly
- [ ] **Export Functions**: Export to file works correctly
- [ ] **Window Resize**: Application resizes properly
- [ ] **Close**: Application closes cleanly

### Size Verification

```bash
# Check executable size
python -c "import os; size=os.path.getsize('dist/FormulaSnap.exe')/(1024*1024); print(f'Size: {size:.2f} MB'); print('OK' if size < 300 else 'TOO LARGE')"
```

### Performance Testing

```powershell
# Test startup time
Measure-Command { dist\FormulaSnap.exe --version }

# Memory usage (run application and check Task Manager)
# Expected: ~200-500MB during operation
```

## Troubleshooting Build Issues

### Common Issues and Solutions

#### 1. ModuleNotFoundError

**Error**: `ModuleNotFoundError: No module named 'X'`

**Solution**: Add the module to `hiddenimports` in `FormulaSnap.spec`:

```python
hiddenimports = [
    # ... existing imports
    'your_missing_module',
]
```

#### 2. Import Errors for PIL/Pillow

**Error**: Issues with PIL/Pillow imports

**Solution**: Ensure Pillow is installed correctly:

```bash
pip uninstall pillow
pip install pillow>=10.0.0
```

#### 3. Tkinter Not Found

**Error**: `No module named '_tkinter'`

**Solution**: Reinstall Python with tcl/tk support enabled, or:

```bash
# Add to hiddenimports in spec file
hiddenimports = [
    'tkinter',
    '_tkinter',
    'tkinter.ttk',
]
```

#### 4. Build Size Too Large

**Error**: Executable exceeds 300MB

**Solution**: 
1. Verify excluded modules in `FormulaSnap.spec`
2. Ensure UPX is enabled: `upx=True`
3. Check that torch/transformers are commented in requirements.txt

```python
# In FormulaSnap.spec, verify these are excluded:
excludes = [
    'matplotlib', 'scipy', 'pandas',
    'jupyter', 'notebook', 'IPython',
]
```

#### 5. Missing DLL Errors

**Error**: Application fails to start due to missing DLLs

**Solution**: Install Visual C++ Redistributable:
- Download from: https://aka.ms/vs/17/release/vc_redist.x64.exe
- Install and rebuild

#### 6. UPX Not Working

**Error**: UPX compression fails

**Solution**: 
1. Download UPX: https://github.com/upx/upx/releases
2. Add to PATH or place in project directory
3. Or disable UPX: Set `upx=False` in spec file

### Debug Build

For troubleshooting, create a debug build:

```python
# In FormulaSnap.spec, change:
exe = EXE(
    # ...
    debug=True,      # Enable debug output
    console=True,    # Show console window
    # ...
)
```

Then rebuild:
```bash
pyinstaller --clean FormulaSnap.spec
```

## Advanced Build Options

### Multi-File Build (Faster Startup)

Edit `FormulaSnap.spec` to create a directory-based distribution:

```python
# After PYZ, replace EXE with:
exe = EXE(
    pyz,
    a.scripts,
    [],  # Leave binaries empty
    exclude_binaries=True,
    # ...
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='FormulaSnap'
)
```

### Adding an Icon

1. Create or obtain a `.ico` file
2. Update `FormulaSnap.spec`:

```python
exe = EXE(
    # ...
    icon='path/to/icon.ico',
)
```

### Code Signing (Optional)

For production releases, sign the executable:

```bash
# Using signtool (requires certificate)
signtool sign /f certificate.pfx /p password /tr http://timestamp.digicert.com dist\FormulaSnap.exe
```

## Continuous Integration

### Local CI Simulation

Test the build as it would run in GitHub Actions:

```bash
# Clean environment
python -m venv ci_test_env
ci_test_env\Scripts\activate

# Install dependencies
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
pip install pyinstaller>=6.0.0

# Build
python scripts/build_exe.py

# Test
dist\FormulaSnap.exe --version

# Cleanup
deactivate
rmdir /s /q ci_test_env
```

## Build Optimization Tips

### Reducing Size

1. **Remove Optional Dependencies**: Keep torch/transformers commented
2. **Enable UPX**: Compresses binaries by 30-50%
3. **Exclude Unused Modules**: Add to `excludes` in spec file
4. **Strip Debug Symbols**: Set `strip=True` (may break on some systems)

### Improving Performance

1. **Lazy Imports**: Import heavy modules only when needed
2. **Multi-threading**: Use threading for long operations
3. **Optimize Image Processing**: Resize images before processing

## Environment Variables

Useful environment variables for building:

```bash
# Disable UPX (if causing issues)
set PYINSTALLER_COMPILE_BOOTLOADER=1

# Set PyInstaller cache location
set PYINSTALLER_CACHE_DIR=%TEMP%\pyinstaller_cache

# Increase recursion limit (if needed)
set PYINSTALLER_RECURSION_LIMIT=5000
```

## Documentation

After building, verify documentation is accurate:

- README.md - Installation and usage
- DEPLOYMENT.md - Deployment procedures
- This BUILD.md - Build instructions
- Code comments - In-code documentation

## Getting Help

If you encounter issues:

1. Check this BUILD.md file
2. Review `scripts/build_exe.py` for automated fixes
3. Check GitHub Issues: https://github.com/YounGuru03/FormulaSnap/issues
4. Create a new issue with:
   - Python version
   - Windows version
   - Full error message
   - Build command used

## Success Checklist

Before considering your build successful:

- [ ] Executable builds without errors
- [ ] Size is under 300MB
- [ ] Application starts within 10 seconds
- [ ] All features work as expected
- [ ] No console window appears (unless debug build)
- [ ] Version command works: `dist\FormulaSnap.exe --version`
- [ ] Can process sample images successfully
- [ ] Memory usage is reasonable (<1GB)
- [ ] No missing DLL errors

## Next Steps

After successful build:

1. Test on a clean Windows machine (if possible)
2. Create GitHub release (see DEPLOYMENT.md)
3. Update documentation if needed
4. Share with testers for feedback

---

**Happy Building!** 🔨

For deployment and release procedures, see [DEPLOYMENT.md](DEPLOYMENT.md)
