# OCR Setup Guide - Tesseract Installation

This guide will help you install Tesseract OCR to enable scanning of image-based PDF documents.

## Windows Installation

### Method 1: Using Pre-built Installer (Recommended)

1. **Download Tesseract installer:**
   - Go to: https://github.com/UB-Mannheim/tesseract/wiki
   - Download the latest Windows installer (e.g., `tesseract-ocr-w64-setup-5.3.3.20231005.exe`)

2. **Install Tesseract:**
   - Run the installer as Administrator
   - Install to default location: `C:\Program Files\Tesseract-OCR`
   - Make sure to check "Add to PATH" during installation

3. **Verify installation:**
   ```cmd
   tesseract --version
   ```

4. **Install additional language packs (optional):**
   - During installation, select additional languages
   - Or download language files from: https://github.com/tesseract-ocr/tessdata
   - Place `.traineddata` files in: `C:\Program Files\Tesseract-OCR\tessdata\`

### Method 2: Using Chocolatey

```powershell
# Install Chocolatey first if not installed
# Then install Tesseract
choco install tesseract

# Install additional languages
choco install tesseract-languages
```

## macOS Installation

### Using Homebrew (Recommended)

```bash
# Install Tesseract
brew install tesseract

# Install additional languages (optional)
brew install tesseract-lang
```

### Using MacPorts

```bash
sudo port install tesseract
```

## Linux Installation

### Ubuntu/Debian

```bash
# Install Tesseract
sudo apt update
sudo apt install tesseract-ocr

# Install additional languages (optional)
sudo apt install tesseract-ocr-vie  # Vietnamese
sudo apt install tesseract-ocr-fra  # French
sudo apt install tesseract-ocr-deu  # German
sudo apt install tesseract-ocr-spa  # Spanish
```

### CentOS/RHEL/Fedora

```bash
# CentOS/RHEL
sudo yum install tesseract

# Fedora
sudo dnf install tesseract
```

## Available Language Codes

Common language codes for OCR:

- `eng` - English (default)
- `vie` - Vietnamese
- `fra` - French  
- `deu` - German
- `spa` - Spanish
- `chi_sim` - Chinese Simplified
- `chi_tra` - Chinese Traditional
- `jpn` - Japanese
- `kor` - Korean
- `ara` - Arabic
- `rus` - Russian

You can combine multiple languages: `eng+vie` for English and Vietnamese.

## Testing Your Installation

1. **Test basic functionality:**
   ```bash
   tesseract --list-langs
   ```

2. **Test with the PDF extractor:**
   ```bash
   python pdf_extractor.py --ocr --ocr-lang eng sample.pdf
   ```

3. **Test with Vietnamese:**
   ```bash
   python pdf_extractor.py --ocr --ocr-lang vie sample_vietnamese.pdf
   ```

## Troubleshooting

### Windows Issues

**Problem:** `tesseract: command not found`
- **Solution:** Add Tesseract to your PATH manually:
  1. Open System Properties → Advanced → Environment Variables
  2. Add `C:\Program Files\Tesseract-OCR` to your PATH
  3. Restart your command prompt

**Problem:** `TesseractNotFoundError`
- **Solution:** Set the tesseract path explicitly in your environment:
  ```cmd
  set TESSDATA_PREFIX=C:\Program Files\Tesseract-OCR\tessdata
  ```

### macOS Issues

**Problem:** Permission denied
- **Solution:** Make sure Tesseract has the correct permissions:
  ```bash
  sudo chmod +x /usr/local/bin/tesseract
  ```

### General Issues

**Problem:** Poor OCR accuracy
- **Solutions:**
  1. Try different language codes
  2. Ensure your PDF has good image quality
  3. Use combined languages: `--ocr-lang eng+vie`
  4. Check that the language pack is installed: `tesseract --list-langs`

**Problem:** Out of memory errors
- **Solution:** Process smaller PDF files or reduce image DPI in the code

## Performance Tips

1. **Use specific languages:** Don't use `--ocr-lang osd` unless necessary
2. **Combine languages wisely:** Only use languages you actually need
3. **Good source material:** Higher quality scans produce better OCR results
4. **Batch processing:** Process multiple files at once for efficiency

## Language Pack Locations

- **Windows:** `C:\Program Files\Tesseract-OCR\tessdata\`
- **macOS:** `/usr/local/share/tessdata/` or `/opt/homebrew/share/tessdata/`
- **Linux:** `/usr/share/tesseract-ocr/*/tessdata/`

Download additional language packs from:
https://github.com/tesseract-ocr/tessdata
