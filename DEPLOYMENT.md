# FormulaSnap Packaging & Deployment Guide

This guide provides comprehensive instructions for packaging, building, and deploying FormulaSnap as a Windows executable.

## Table of Contents
1. [Development Setup](#development-setup)
2. [Building the Executable](#building-the-executable)
3. [Size Optimization](#size-optimization)
4. [Testing and Validation](#testing-and-validation)
5. [GitHub Actions Deployment](#github-actions-deployment)
6. [Manual Release Process](#manual-release-process)
7. [Troubleshooting](#troubleshooting)

## Development Setup

### Prerequisites
- **Windows 10/11** (for native builds)
- **Python 3.8-3.11** (3.10 recommended)
- **Git** for version control
- **4GB RAM minimum** (8GB recommended for building)

### Initial Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YounGuru03/FormulaSnap.git
   cd FormulaSnap
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Test the application**:
   ```bash
   python -m formulasnap.main
   ```

## Building the Executable

### Automated Build (Recommended)

Use the provided build script for optimal results:

```bash
python scripts/build_exe.py
```

This script will:
- Clean previous builds
- Install PyInstaller if needed
- Configure optimal build settings
- Generate the executable
- Test basic functionality

### Manual Build Process

If you need more control over the build process:

1. **Install PyInstaller**:
   ```bash
   pip install pyinstaller
   ```

2. **Clean previous builds**:
   ```bash
   rmdir /s build dist
   del *.spec.bak
   ```

3. **Build using spec file**:
   ```bash
   pyinstaller --clean --noconfirm FormulaSnap.spec
   ```

4. **Verify the build**:
   ```bash
   dist\FormulaSnap.exe --version
   ```

### Build Configuration

The `FormulaSnap.spec` file contains optimized settings:

- **Single file executable**: Everything bundled into one .exe
- **Windows subsystem**: No console window (GUI only)
- **UPX compression**: Reduces file size
- **Excluded modules**: Removes unnecessary dependencies
- **Hidden imports**: Ensures all required modules are included

## Size Optimization

### Target Size: Under 300MB

Current optimization strategies:

1. **Excluded Heavy Dependencies**:
   ```python
   excluded_modules = [
       'matplotlib', 'scipy', 'pandas', 'jupyter',
       'notebook', 'IPython', 'zmq', 'PyQt5', 'PyQt6'
   ]
   ```

2. **UPX Compression**:
   - Enabled in spec file: `upx=True`
   - Reduces executable size by 30-50%

3. **Selective Imports**:
   - Only include necessary torch/transformers components
   - Use lightweight alternatives where possible

4. **Data Optimization**:
   - Compress model files
   - Remove unnecessary language packs
   - Exclude test files and documentation

### Size Verification

Check executable size after build:

```bash
python -c "
import os
size_mb = os.path.getsize('dist/FormulaSnap.exe') / (1024*1024)
print(f'Executable size: {size_mb:.2f} MB')
if size_mb > 300:
    print('WARNING: Size exceeds 300MB limit!')
else:
    print('Size OK: Under 300MB limit')
"
```

## Testing and Validation

### Pre-Release Testing

1. **Functionality Tests**:
   ```bash
   # Test CLI
   dist\FormulaSnap.exe --version
   dist\FormulaSnap.exe --help
   
   # Test GUI (manual)
   dist\FormulaSnap.exe
   ```

2. **Performance Tests**:
   - Launch time (should be < 10 seconds)
   - Memory usage (should be < 1GB)
   - Processing speed (formulas in < 30 seconds)

3. **Compatibility Tests**:
   - Test on Windows 10 and 11
   - Test with different screen resolutions
   - Test clipboard functionality
   - Test file import/export

### Automated Testing

Run the test suite before building:

```bash
python -m pytest tests/ -v
```

## GitHub Actions Deployment

### Automatic Builds

The `.github/workflows/build.yml` workflow automatically:

1. **Triggers on**:
   - Push to `main` branch
   - Tagged releases (`v*`)
   - Pull requests

2. **Build Process**:
   - Sets up Windows environment
   - Installs dependencies
   - Builds executable
   - Runs tests
   - Uploads artifacts

3. **Release Process**:
   - Creates GitHub release for tags
   - Uploads executable as release asset
   - Generates release notes

### Triggering a Release

1. **Create and push a tag**:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

2. **GitHub Actions will**:
   - Build the executable
   - Create a release
   - Upload the .exe file
   - Generate release notes

### Monitoring Builds

- Check build status at: `https://github.com/YounGuru03/FormulaSnap/actions`
- Build artifacts available for 7 days
- Release assets permanent

## Manual Release Process

### Creating a Release

1. **Prepare the release**:
   ```bash
   # Update version in relevant files
   # Test thoroughly
   # Build and test executable
   python scripts/build_exe.py
   ```

2. **Create GitHub release**:
   - Go to GitHub repository
   - Click "Releases" → "Create a new release"
   - Choose tag version (e.g., `v1.0.0`)
   - Upload `dist/FormulaSnap.exe`
   - Write release notes

3. **Release checklist**:
   - [ ] Version numbers updated
   - [ ] Executable tested on clean Windows system
   - [ ] Size under 300MB
   - [ ] All features working
   - [ ] Documentation updated
   - [ ] Release notes written

### Distribution

1. **Primary Distribution**: GitHub Releases
2. **Alternative Options**:
   - Direct download links
   - Package managers (future)
   - Corporate distribution (if needed)

## Troubleshooting

### Common Build Issues

**"Module not found" errors**:
```bash
# Add to hiddenimports in FormulaSnap.spec
hiddenimports = [
    'your_missing_module',
    # ... other imports
]
```

**Size too large**:
```bash
# Add to excludes in FormulaSnap.spec
excludes = [
    'large_unused_module',
    # ... other excludes
]
```

**Missing DLLs**:
```bash
# Check with Dependency Walker or similar
# Add to binaries in FormulaSnap.spec if needed
```

### Runtime Issues

**"Application failed to start"**:
- Check Windows version compatibility
- Verify all required Visual C++ redistributables
- Try running as administrator

**Slow startup**:
- Check antivirus software interference
- Ensure SSD storage for better performance
- Verify adequate RAM

### Development Issues

**Import errors during development**:
```bash
# Ensure virtual environment is activated
venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

**GUI not responding**:
- Check for blocking operations in main thread
- Verify image processing is in background thread
- Test clipboard access permissions

## Performance Optimization

### Startup Time
- Lazy load heavy dependencies
- Use threading for initialization
- Implement splash screen for user feedback

### Memory Usage
- Process images in chunks for large files
- Clear intermediate processing results
- Use memory-mapped files for large datasets

### Processing Speed
- Optimize image preprocessing pipeline
- Use appropriate image resizing
- Implement progress callbacks

## Advanced Deployment Options

### Corporate Deployment
- Code signing certificates
- Group Policy distribution
- Silent installation options

### Updates and Versioning
- Implement auto-update mechanism
- Version checking against GitHub releases
- Backward compatibility considerations

---

## Contact and Support

For deployment issues:
- Open GitHub issue with build logs
- Check existing issues and documentation
- Provide system specifications and error details

**Happy deploying!** 🚀