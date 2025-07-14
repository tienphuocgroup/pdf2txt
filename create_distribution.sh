#!/bin/bash

# Create Distribution Package
# Packages the PDF extractor for company-wide distribution

set -e

echo "📦 Creating distribution package..."

# Create distribution directory
DIST_DIR="PDF-Extractor-Distribution"
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

# Copy executables if they exist
if [ -f "dist/pdf-extractor-macos" ]; then
    echo "✅ Adding macOS executable..."
    cp "dist/pdf-extractor-macos" "$DIST_DIR/"
    chmod +x "$DIST_DIR/pdf-extractor-macos"
fi

if [ -f "dist/pdf-extractor-windows.exe" ]; then
    echo "✅ Adding Windows executable..."
    cp "dist/pdf-extractor-windows.exe" "$DIST_DIR/"
fi

# Copy documentation
echo "📄 Adding documentation..."
cp "USER_GUIDE.md" "$DIST_DIR/"
cp "README.md" "$DIST_DIR/"

# Create quick start script for macOS
cat > "$DIST_DIR/quick-start-macos.sh" << 'EOF'
#!/bin/bash
# Quick Start Guide for macOS Users

echo "PDF Text & Image Extractor - Quick Start"
echo "========================================"
echo
echo "Usage examples:"
echo "  ./pdf-extractor-macos document.pdf"
echo "  ./pdf-extractor-macos *.pdf"
echo "  ./pdf-extractor-macos file1.pdf file2.pdf -o /path/to/output"
echo
echo "For full documentation, see USER_GUIDE.md"
echo
echo "Ready to extract PDFs!"
EOF

chmod +x "$DIST_DIR/quick-start-macos.sh"

# Create quick start script for Windows
cat > "$DIST_DIR/quick-start-windows.bat" << 'EOF'
@echo off
echo PDF Text ^& Image Extractor - Quick Start
echo ========================================
echo.
echo Usage examples:
echo   pdf-extractor-windows.exe document.pdf
echo   pdf-extractor-windows.exe *.pdf
echo   pdf-extractor-windows.exe file1.pdf file2.pdf -o C:\path\to\output
echo.
echo For full documentation, see USER_GUIDE.md
echo.
echo Ready to extract PDFs!
echo.
pause
EOF

# Create README for distribution
cat > "$DIST_DIR/DISTRIBUTION_README.txt" << 'EOF'
PDF Text & Image Extractor - Company Distribution
================================================

This package contains single-file executables for extracting text and images from PDF files.

Files Included:
- pdf-extractor-macos        : macOS executable (Intel + Apple Silicon)
- pdf-extractor-windows.exe  : Windows executable (64-bit)
- USER_GUIDE.md             : Complete user documentation
- README.md                 : Technical documentation
- quick-start-macos.sh      : Quick start guide for macOS
- quick-start-windows.bat   : Quick start guide for Windows

Quick Start:
1. Copy the appropriate executable to your computer
2. Open terminal/command prompt
3. Run: ./pdf-extractor-macos document.pdf (macOS)
   Or:  pdf-extractor-windows.exe document.pdf (Windows)

No installation required - these are standalone executables!

For complete documentation, see USER_GUIDE.md

Features:
✅ Extract text and images from any PDF
✅ Smart text splitting for AI processing
✅ Batch processing support
✅ Handles complex image formats
✅ Cross-platform compatibility
✅ No installation required

Support:
- Read USER_GUIDE.md for detailed instructions
- Use --help flag for command line options
- Check file permissions if you encounter issues
EOF

# Get package size
PACKAGE_SIZE=$(du -sh "$DIST_DIR" | cut -f1)

echo "✅ Distribution package created successfully!"
echo "📦 Location: $(pwd)/$DIST_DIR"
echo "📏 Package size: $PACKAGE_SIZE"
echo ""
echo "Contents:"
ls -la "$DIST_DIR"
echo ""
echo "🚀 Ready for company distribution!"
echo "   Share the entire '$DIST_DIR' folder with users"