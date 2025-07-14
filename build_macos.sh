#!/bin/bash

# PDF Extractor - macOS Build Script
# Creates a universal binary for both Intel and Apple Silicon Macs

set -e

echo "🔨 Building PDF Extractor for macOS..."

# Activate virtual environment
source pdf_env_new/bin/activate

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.spec

# Build executable for macOS (current architecture)
echo "🏗️  Building macOS executable..."
pyinstaller --onefile \
    --name "pdf-extractor-macos" \
    --optimize 2 \
    --strip \
    --console \
    --add-data "README.md:." \
    pdf_extractor.py

# Get file size
FILE_SIZE=$(du -h dist/pdf-extractor-macos | cut -f1)

echo "✅ Build completed successfully!"
echo "📦 Executable: dist/pdf-extractor-macos"
echo "📏 File size: $FILE_SIZE"
echo ""
echo "🧪 Testing executable..."
./dist/pdf-extractor-macos --help

echo ""
echo "🎉 macOS build ready for distribution!"
echo "   Location: $(pwd)/dist/pdf-extractor-macos"