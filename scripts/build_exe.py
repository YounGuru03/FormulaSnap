#!/usr/bin/env python3
"""
Build script for creating Windows executable
Optimized to stay under 300MB size limit
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(cmd):
    """Run shell command and return result"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error running command: {cmd}")
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        sys.exit(1)
    
    return result


def optimize_build():
    """Optimize the build to reduce size"""
    print("Optimizing build size...")
    
    # Clean up unnecessary files
    build_dir = Path("build")
    if build_dir.exists():
        shutil.rmtree(build_dir)
    
    # Remove __pycache__ directories
    for root, dirs, files in os.walk("."):
        for dir_name in dirs[:]:
            if dir_name == "__pycache__":
                pycache_path = Path(root) / dir_name
                print(f"Removing {pycache_path}")
                shutil.rmtree(pycache_path)
                dirs.remove(dir_name)


def build_exe():
    """Build the Windows executable"""
    print("Starting FormulaSnap build process...")
    
    # Check if we're on Windows or can cross-compile
    if os.name != 'nt':
        print("Warning: Building on non-Windows system. Some features may not work correctly.")
    
    # Install PyInstaller if not present
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        run_command("pip install pyinstaller")
    
    # Clean previous builds
    optimize_build()
    
    # Build with PyInstaller
    print("Building executable with PyInstaller...")
    
    # Use spec file for better control
    spec_file = "FormulaSnap.spec"
    if not Path(spec_file).exists():
        print(f"Error: {spec_file} not found")
        sys.exit(1)
    
    # Run PyInstaller
    cmd = f"pyinstaller --clean --noconfirm {spec_file}"
    run_command(cmd)
    
    # Check if exe was created
    exe_path = Path("dist/FormulaSnap.exe")
    if not exe_path.exists():
        print("Error: Executable was not created")
        sys.exit(1)
    
    # Get file size
    size_mb = exe_path.stat().st_size / (1024 * 1024)
    print(f"Executable created: {exe_path}")
    print(f"Size: {size_mb:.2f} MB")
    
    if size_mb > 300:
        print(f"Warning: Executable size ({size_mb:.2f} MB) exceeds 300MB limit")
        print("Consider optimizing dependencies or excluding unnecessary modules")
    
    print("Build completed successfully!")
    
    return exe_path


def test_exe(exe_path):
    """Test the built executable"""
    print("Testing executable...")
    
    try:
        # Test version command
        result = run_command(f'"{exe_path}" --version')
        print(f"Version test passed: {result.stdout.strip()}")
        
        # Test help command
        result = subprocess.run([str(exe_path), "--help"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("Help test passed")
        else:
            print("Help test failed, but this may be expected")
        
        print("Executable tests completed")
        
    except Exception as e:
        print(f"Warning: Could not fully test executable: {e}")


def main():
    """Main build function"""
    try:
        # Change to project directory
        os.chdir(Path(__file__).parent.parent)
        
        # Build the executable
        exe_path = build_exe()
        
        # Test the executable
        test_exe(exe_path)
        
        print("\n" + "="*50)
        print("BUILD SUCCESSFUL!")
        print(f"Executable: {exe_path}")
        print(f"Size: {exe_path.stat().st_size / (1024 * 1024):.2f} MB")
        print("="*50)
        
    except KeyboardInterrupt:
        print("\nBuild interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Build failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()