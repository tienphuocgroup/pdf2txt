# PDF to Text and Image Extractor with OCR Support

A robust, cross-platform Python script that extracts text content and images from PDF files, with intelligent colorspace handling, OCR support for scanned documents, and token-based text splitting. Handles complex PDFs with CMYK, DeviceN, and other colorspaces that commonly cause extraction failures.

## Features

- **Robust Text Extraction**: Extract all text content from PDF files with page markers
- **🆕 OCR Support**: Extract text from scanned PDF documents using Tesseract OCR
  - Automatic detection of scanned pages (image-based content)
  - Support for multiple languages (English, Vietnamese, French, German, Spanish, etc.)
  - Intelligent combination of PDF text and OCR text
  - High-resolution rendering for better OCR accuracy
- **Advanced Image Extraction**: Extract all images with intelligent colorspace handling
  - Supports CMYK, DeviceN, RGB, and grayscale colorspaces
  - Automatic conversion to PNG-compatible formats
  - Handles complex PDFs that cause other extractors to fail
  - OCR text extraction from individual images
- **Smart Integration**: Insert image filenames at the correct positions within the extracted text
- **Token-based Splitting**: Split large documents into chunks of approximately 45,000 tokens each
- **Cross-platform**: Works on both macOS and Windows
- **Dual Interface**: Command-line and GUI versions available
- **Latest Libraries**: Uses PyMuPDF 1.26.3, tiktoken 0.9.0, and Tesseract OCR

## Requirements

- Python 3.9 or higher
- PyMuPDF 1.26.3+ (for PDF processing)
- tiktoken 0.9.0+ (for token counting)
- **For OCR features:**
  - pytesseract 0.3.10+ (Python wrapper for Tesseract)
  - Pillow 10.0.0+ (image processing)
  - Tesseract OCR engine (see [TESSERACT_SETUP.md](TESSERACT_SETUP.md) for installation)

## Installation

### Step 1: Clone or Download the Script

Download the following files to your project directory:
- `pdf_extractor.py`
- `requirements.txt`

### Step 2: Set Up Virtual Environment

#### On macOS:
```bash
# Navigate to your project directory
cd /path/to/your/project

# Create virtual environment
python3 -m venv pdf_env

# Activate virtual environment
source pdf_env/bin/activate

# Install dependencies
python3 -m pip install -r requirements.txt
```

#### On Windows:
```cmd
# Navigate to your project directory
cd C:\path\to\your\project

# Create virtual environment
python -m venv pdf_env

# Activate virtual environment
pdf_env\Scripts\activate

# Install dependencies
python -m pip install -r requirements.txt
```

### Step 3: Verify Installation

Test that the required libraries are installed correctly:

#### On macOS:
```bash
source pdf_env/bin/activate
python3 -c "import fitz; import tiktoken; print('Dependencies installed successfully!')"
```

#### On Windows:
```cmd
pdf_env\Scripts\activate
python -c "import fitz; import tiktoken; print('Dependencies installed successfully!')"
```

## Usage

### Basic Usage

#### On macOS:
```bash
# Activate virtual environment
source pdf_env/bin/activate

# Extract from PDF (creates output directory automatically)
python3 pdf_extractor.py path/to/your/document.pdf
```

#### On Windows:
```cmd
# Activate virtual environment
pdf_env\Scripts\activate

# Extract from PDF (creates output directory automatically)
python pdf_extractor.py path\to\your\document.pdf
```

### Advanced Usage

#### Specify Output Directory

```bash
# macOS
python3 pdf_extractor.py document.pdf -o /path/to/output/directory

# Windows
python pdf_extractor.py document.pdf -o C:\path\to\output\directory
```

#### Customize Token Limit

```bash
# macOS - Split into 30k token chunks instead of 45k
python3 pdf_extractor.py document.pdf -t 30000

# Windows - Split into 30k token chunks instead of 45k
python pdf_extractor.py document.pdf -t 30000
```

#### Complete Example

```bash
# macOS
python3 pdf_extractor.py my_document.pdf -o extracted_content -t 40000

# Windows
python pdf_extractor.py my_document.pdf -o extracted_content -t 40000
```

### Command Line Options

```
usage: pdf_extractor.py [-h] [-o OUTPUT] [-t MAX_TOKENS] [-b] [--ocr] [--ocr-lang OCR_LANG] pdf_path [pdf_path ...]

Extract text and images from PDF with token splitting and OCR support

positional arguments:
  pdf_path              Path to PDF file(s) - supports multiple files and wildcards

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output directory (default: {pdf_name}_extracted for each file)
  -t MAX_TOKENS, --max-tokens MAX_TOKENS
                        Maximum tokens per output file (default: 45000)
  -b, --batch           Batch mode: put all files in single output directory
  --ocr                 Enable OCR for scanned documents (requires Tesseract)
  --ocr-lang OCR_LANG   OCR language code (default: eng). Examples: vie (Vietnamese), eng+vie (multiple)
```

positional arguments:
  pdf_path              Path to the PDF file

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output directory (default: {pdf_name}_extracted)
  -t MAX_TOKENS, --max-tokens MAX_TOKENS
                        Maximum tokens per output file (default: 45000)
```

## Output Structure

The script creates the following output structure:

```
output_directory/
├── document_name.txt                 # Single text file (if under token limit)
├── document_name_part_1.txt          # First part (if split required)
├── document_name_part_2.txt          # Second part (if split required)
└── extracted_images/
    ├── page_1_image_1.png
    ├── page_1_image_2.png
    ├── page_2_image_1.png
    └── ...
```

### Text File Format

The extracted text files follow this format:

```
--- Page 1 ---
[IMAGE: page_1_image_1.png]
[IMAGE: page_1_image_2.png]

Text content from page 1...

--- Page 2 ---
[IMAGE: page_2_image_1.png]

Text content from page 2...
```

### Image Naming Convention

Images are named using the pattern: `page_{page_number}_image_{image_index}.png`

- `page_1_image_1.png` - First image from page 1
- `page_1_image_2.png` - Second image from page 1
- `page_2_image_1.png` - First image from page 2

## Examples

### Example 1: Simple Extraction

```bash
# macOS
source pdf_env/bin/activate
python3 pdf_extractor.py report.pdf

# Windows
pdf_env\Scripts\activate
python pdf_extractor.py report.pdf
```

**Output:**
```
Processing: report.pdf
Output directory: report_extracted
Created: report_extracted/report.txt (15,432 tokens)

==================================================
EXTRACTION COMPLETE
==================================================
PDF: report.pdf
Output directory: report_extracted
Text files created: 1
Images extracted: 8
Total tokens: 15,432

Text files:
  - report_extracted/report.txt
```

### Example 2: Large Document with Splitting

```bash
# macOS
python3 pdf_extractor.py large_document.pdf -t 20000

# Windows
python pdf_extractor.py large_document.pdf -t 20000
```

**Output:**
```
Processing: large_document.pdf
Output directory: large_document_extracted
Created: large_document_extracted/large_document_part_1.txt (19,876 tokens)
Created: large_document_extracted/large_document_part_2.txt (18,543 tokens)
Created: large_document_extracted/large_document_part_3.txt (12,098 tokens)

==================================================
EXTRACTION COMPLETE
==================================================
PDF: large_document.pdf
Output directory: large_document_extracted
Text files created: 3
Images extracted: 45
Total tokens: 50,517

Text files:
  - large_document_extracted/large_document_part_1.txt
  - large_document_extracted/large_document_part_2.txt
  - large_document_extracted/large_document_part_3.txt
```

### OCR Support for Scanned Documents

#### Setup OCR (One-time)
See [TESSERACT_SETUP.md](TESSERACT_SETUP.md) for detailed Tesseract installation instructions.

#### Basic OCR Usage

```bash
# macOS - Enable OCR for scanned documents
python3 pdf_extractor.py document.pdf --ocr

# Windows - Enable OCR for scanned documents  
python pdf_extractor.py document.pdf --ocr
```

#### OCR with Different Languages

```bash
# Vietnamese documents
python3 pdf_extractor.py document.pdf --ocr --ocr-lang vie

# Multiple languages (English + Vietnamese)
python3 pdf_extractor.py document.pdf --ocr --ocr-lang eng+vie

# French documents
python3 pdf_extractor.py document.pdf --ocr --ocr-lang fra
```

#### Complete OCR Example

```bash
# Process scanned Vietnamese document with custom settings
python3 pdf_extractor.py scanned_document.pdf --ocr --ocr-lang eng+vie -o vietnamese_output -t 30000
```

### GUI Version

For a user-friendly graphical interface:

```bash
# macOS
python3 pdf_extractor_gui.py

# Windows
python pdf_extractor_gui.py
```

The GUI includes:
- File selection with drag & drop
- OCR language selection
- Real-time progress tracking
- Batch processing support
- Integrated error logging

## Troubleshooting

### Common Issues

#### 1. "No module named 'fitz'" Error

**Solution**: Make sure you've activated the virtual environment and installed dependencies:

```bash
# macOS
source pdf_env/bin/activate
python3 -m pip install -r requirements.txt

# Windows
pdf_env\Scripts\activate
python -m pip install -r requirements.txt
```

#### 2. "externally-managed-environment" Error

**Solution**: Use a virtual environment (don't install system-wide):

```bash
# Create and use virtual environment as shown in installation steps
python3 -m venv pdf_env
source pdf_env/bin/activate  # macOS
# or
pdf_env\Scripts\activate     # Windows
```

#### 3. "PDF file not found" Error

**Solution**: Check the file path and ensure the PDF file exists:

```bash
# Use absolute path
python3 pdf_extractor.py /full/path/to/document.pdf

# Or navigate to the directory containing the PDF
cd /path/to/pdf/directory
python3 pdf_extractor.py document.pdf
```

#### 4. Permission Denied Error

**Solution**: Ensure you have write permissions to the output directory:

```bash
# Specify a different output directory
python3 pdf_extractor.py document.pdf -o ~/Desktop/pdf_output
```

#### 5. Memory Issues with Large PDFs

**Solution**: Use a smaller token limit to create more, smaller files:

```bash
# Reduce token limit for large documents
python3 pdf_extractor.py large_document.pdf -t 25000
```

### Performance Tips

1. **For large PDFs**: Use smaller token limits (20,000-30,000) to create more manageable files
2. **For many images**: Ensure sufficient disk space in the output directory
3. **For batch processing**: Process files one at a time to avoid memory issues

## Dependencies Information

### PyMuPDF 1.26.3
- **Purpose**: PDF processing and image extraction
- **Platform Support**: Windows (32/64-bit), macOS (Intel/Apple Silicon), Linux
- **Installation**: Pre-built wheels available via pip
- **License**: Open source

### tiktoken 0.9.0
- **Purpose**: Token counting for text splitting
- **Platform Support**: Windows, macOS, Linux
- **Installation**: Pre-built wheels available via pip
- **License**: Open source

## Version Information

- **Script Version**: 1.0.0
- **Python Support**: 3.9+
- **Last Updated**: July 2025
- **Cross-platform**: ✅ macOS and Windows

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all dependencies are installed correctly
3. Ensure you're using the correct Python version (3.9+)
4. Make sure the virtual environment is activated

## License

This script uses open-source libraries and is provided as-is for educational and practical use.