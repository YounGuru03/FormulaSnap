#!/usr/bin/env python3
"""
Setup script for FormulaSnap
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="formulasnap",
    version="1.0.0",
    author="FormulaSnap Team",
    description="Lightweight offline Windows tool for OCR of math formulas",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pillow>=10.0.0",
        "opencv-python>=4.8.0",
        "numpy>=1.24.0",
        "pix2tex>=0.1.2",
        "transformers>=4.30.0",
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "pyperclip>=1.8.2",
    ],
    entry_points={
        "console_scripts": [
            "formulasnap=formulasnap.main:main",
        ],
    },
)