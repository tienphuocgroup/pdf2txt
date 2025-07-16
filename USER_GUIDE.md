# PDF Text & Image Extractor - User Guide

## Overview

The PDF Text & Image Extractor is a powerful, single-file application that extracts text content and images from PDF files. It automatically splits large documents into manageable chunks and handles complex image formats that other tools often fail to process.

## Quick Start

### macOS
```bash
# Extract a single PDF
./pdf-extractor-macos document.pdf

# Extract multiple PDFs
./pdf-extractor-macos file1.pdf file2.pdf file3.pdf

# Extract all PDFs in current directory
./pdf-extractor-macos *.pdf
```

### Windows
```cmd
# Extract a single PDF
pdf-extractor-windows.exe document.pdf

# Extract multiple PDFs
pdf-extractor-windows.exe file1.pdf file2.pdf file3.pdf

# Extract all PDFs in current directory
pdf-extractor-windows.exe *.pdf
```

## Features

### ✅ What It Does
- **Text Extraction**: Extracts clean, readable text from PDF files
- **Image Extraction**: Saves all images as PNG files with proper colorspace conversion
- **Smart Splitting**: Divides large documents into ~45,000 token chunks for AI processing
- **Batch Processing**: Process multiple PDF files at once
- **Error Recovery**: Gracefully handles corrupted images and complex PDF structures
- **Cross-Platform**: Works on both macOS and Windows

### 🎯 Perfect For
- Converting PDFs for AI analysis (ChatGPT, Claude, etc.)
- Extracting images from complex documents
- Processing large document collections
- Handling PDFs with problematic image formats (CMYK, DeviceN, etc.)

## Command Line Options

```bash
pdf-extractor [OPTIONS] PDF_FILE [PDF_FILE ...]

Positional Arguments:
  PDF_FILE              Path to PDF file(s) - supports multiple files and wildcards

Options:
  -h, --help            Show help message and exit
  -o, --output OUTPUT   Output directory (default: {pdf_name}_extracted for each file)
  -t, --max-tokens MAX_TOKENS
                        Maximum tokens per output file (default: 45000)
  -b, --batch           Batch mode: put all files in single output directory
```

## Usage Examples

### Basic Usage
```bash
# Extract single PDF to default location
./pdf-extractor-macos report.pdf

# Extract with custom output directory
./pdf-extractor-macos report.pdf -o /Users/john/Documents/extracted

# Extract with custom token limit
./pdf-extractor-macos report.pdf -t 30000
```

### Batch Processing
```bash
# Process all PDFs in current directory
./pdf-extractor-macos *.pdf

# Process specific files
./pdf-extractor-macos file1.pdf file2.pdf file3.pdf

# Batch mode - all files in single output directory
./pdf-extractor-macos *.pdf -b -o /Users/john/Documents/all_extracted
```

### Advanced Examples
```bash
# Process PDFs from multiple directories
./pdf-extractor-macos ~/Documents/*.pdf ~/Downloads/*.pdf

# Process with specific settings
./pdf-extractor-macos *.pdf -t 60000 -o ./extracted_docs
```

## Output Structure

For a PDF named `document.pdf`, the extractor creates:

```
document_extracted/
├── document.txt (or document_part_1.txt, document_part_2.txt if split)
└── extracted_images/
    ├── page_1_image_1.png
    ├── page_1_image_2.png
    ├── page_2_image_1.png
    └── ...
```

### Output Files
- **Text Files**: Clean, readable text with image references inserted at correct positions
- **Image Files**: All images converted to PNG format with proper colorspace handling
- **Error Files**: If an image cannot be processed, an error file is created instead

## Text Processing Features

### Automatic Cleanup
- Removes PDF extraction artifacts
- Fixes broken words split across lines
- Normalizes spacing and punctuation
- Removes page numbers and formatting artifacts

### Smart Splitting
- Uses GPT-4 tokenizer for accurate token counting
- Splits on logical boundaries (sentences, paragraphs)
- Maintains readability across chunks
- Perfect for AI processing workflows

### Image Integration
- Inserts `[IMAGE: filename.png]` references at correct positions
- Preserves document structure and flow
- Makes it easy to correlate text with images

## Troubleshooting

### Common Issues

**"No PDF files found!"**
- Check file paths and extensions
- Ensure PDF files actually exist
- Use absolute paths if relative paths don't work

**"Permission denied"**
- Ensure you have read access to PDF files
- Ensure you have write access to output directory
- Try running from a different directory

**"Image conversion errors"**
- These are usually non-fatal warnings
- The extractor will create error files instead
- Text extraction will continue normally

### Performance Tips

**For Large Documents:**
- Use smaller token limits (`-t 30000`) for faster processing
- Ensure sufficient disk space for output files
- Consider processing files individually rather than in batch

**For Many Files:**
- Use batch mode (`-b`) for better organization
- Process in smaller groups if memory is limited
- Monitor disk space during processing

## Technical Details

### System Requirements
- **macOS**: 10.14 (Mojave) or later, Intel or Apple Silicon
- **Windows**: Windows 10 or later, 64-bit
- **Disk Space**: ~50MB for application, variable for output
- **Memory**: 512MB minimum, 2GB recommended for large files

### File Format Support
- **Input**: PDF files (any version)
- **Output**: Plain text (.txt), PNG images
- **Colorspaces**: RGB, CMYK, Grayscale, DeviceN, and more

### Token Counting
- Uses OpenAI's `cl100k_base` encoding (GPT-4)
- Default limit: 45,000 tokens (~32,000 words)
- Adjustable via command line option

## Support

### Getting Help
- Use `--help` flag for command line options
- Check this user guide for common issues
- Verify file permissions and paths

### Reporting Issues
- Note the exact command used
- Include error messages if any
- Specify operating system and PDF details

## Distribution

### Company Installation
1. Download the appropriate executable for your platform
2. Place in a convenient location (e.g., `/Applications/` on macOS)
3. Make executable if necessary (macOS: `chmod +x pdf-extractor-macos`)
4. Add to PATH for global access (optional)

### No Installation Required
- Single executable file
- No Python or dependencies needed
- Works on clean systems
- Portable across machines

---

*This tool is designed for defensive security and document processing use cases. It helps extract and analyze PDF content in a safe, controlled manner.*

## OCR Support for Scanned Documents

### 🆕 NEW FEATURE: OCR Integration

The PDF Extractor now supports OCR (Optical Character Recognition) to extract text from scanned PDF documents that contain images instead of searchable text.

### OCR Features

- **Automatic Detection**: Automatically detects pages with little extractable text (likely scanned)
- **Multi-language Support**: Supports 100+ languages including English, Vietnamese, French, German, Spanish
- **Smart Processing**: Combines PDF text with OCR text for best results
- **Image OCR**: Extracts text from individual images within PDFs
- **High Accuracy**: Uses high-resolution rendering for better OCR accuracy

### Setup OCR (One-time)

1. **Install Tesseract OCR engine** (see [TESSERACT_SETUP.md](TESSERACT_SETUP.md))
2. **Install Python packages** (already included in requirements.txt):
   ```bash
   pip install pytesseract Pillow
   ```

### Using OCR

#### Command Line

```bash
# Basic OCR (English)
./pdf-extractor-macos document.pdf --ocr

# Vietnamese documents
./pdf-extractor-macos document.pdf --ocr --ocr-lang vie

# Multiple languages
./pdf-extractor-macos document.pdf --ocr --ocr-lang eng+vie
```

#### GUI Version

1. Launch the GUI: `python pdf_extractor_gui.py`
2. Check "Enable OCR for scanned documents"
3. Select your language from the dropdown
4. Process your files normally

### Supported Languages

Common language codes:
- `eng` - English (default)
- `vie` - Vietnamese  
- `fra` - French
- `deu` - German
- `spa` - Spanish
- `chi_sim` - Chinese Simplified
- `jpn` - Japanese
- `kor` - Korean
- `ara` - Arabic

See full list: `tesseract --list-langs`

### Performance Tips

1. **Use specific languages**: Only specify languages you need
2. **Good quality scans**: Higher resolution = better OCR results
3. **Combine languages**: Use `eng+vie` for bilingual documents
4. **Test first**: Run on a sample page to verify language detection