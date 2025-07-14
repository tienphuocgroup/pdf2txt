#!/bin/bash

# PDF Extractor GUI - macOS Build Script
# Creates a macOS application bundle with GUI

set -e

echo "🔨 Building PDF Extractor GUI for macOS..."

# Activate virtual environment
source pdf_env_new/bin/activate

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.spec

# Build GUI application for macOS
echo "🏗️  Building GUI application..."
pyinstaller --onefile \
    --windowed \
    --name "PDF-Extractor-GUI" \
    --optimize 2 \
    --strip \
    --add-data "README.md:." \
    --icon-file="" \
    pdf_extractor_gui.py

# Get file size
FILE_SIZE=$(du -h dist/PDF-Extractor-GUI | cut -f1)

echo "✅ Build completed successfully!"
echo "📦 Application: dist/PDF-Extractor-GUI"
echo "📏 File size: $FILE_SIZE"
echo ""

echo "🎉 GUI application ready for distribution!"
echo "   Location: $(pwd)/dist/PDF-Extractor-GUI"
echo "   Note: This is a GUI application - double-click to run"