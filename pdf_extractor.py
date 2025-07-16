#!/usr/bin/env python3
"""
PDF Text and Image Extractor with Token Splitting and OCR Support
Extracts text content and images from PDF files, with OCR support for scanned documents,
inserting image filenames at correct positions in text, and splits output into ~45k token chunks.
"""

import os
import sys
import fitz  # PyMuPDF
import argparse
from pathlib import Path
from typing import List, Tuple, Dict
import re
import tiktoken
import pytesseract
from PIL import Image
import io

class PDFExtractor:
    def __init__(self, max_tokens: int = 45000, use_ocr: bool = False, ocr_language: str = 'eng'):
        self.max_tokens = max_tokens
        self.use_ocr = use_ocr
        self.ocr_language = ocr_language
        self.encoding = tiktoken.get_encoding("cl100k_base")  # GPT-4 encoding
        
        # Test tesseract availability if OCR is enabled
        if self.use_ocr:
            try:
                pytesseract.get_tesseract_version()
                print(f"✓ Tesseract OCR enabled (language: {ocr_language})")
            except Exception as e:
                print(f"⚠ Warning: Tesseract OCR not available: {e}")
                print("  OCR features will be disabled. Install Tesseract to enable OCR.")
                self.use_ocr = False
        
    def count_tokens(self, text: str) -> int:
        """Count tokens in text using tiktoken"""
        return len(self.encoding.encode(text))
    
    def clean_extracted_text(self, text: str) -> str:
        """Clean and improve text quality by fixing common PDF extraction issues"""
        # Remove excessive whitespace and normalize spaces
        text = re.sub(r'[ \t]+', ' ', text)
        
        # Fix broken words that were split across lines (common in PDFs)
        # Look for words ending with hyphen followed by newline and lowercase letter
        text = re.sub(r'-\n([a-z])', r'\1', text)
        
        # Remove single character lines that are likely formatting artifacts
        text = re.sub(r'\n[a-zA-Z]\n', '\n', text)
        
        # Fix multiple consecutive newlines (more than 2)
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove trailing spaces at end of lines
        text = re.sub(r' +\n', '\n', text)
        
        # Fix common spacing issues around punctuation
        text = re.sub(r' +([,.!?;:])', r'\1', text)
        text = re.sub(r'([,.!?;:])([A-Z])', r'\1 \2', text)
        
        # Remove isolated numbers/characters that are likely page numbers or artifacts
        text = re.sub(r'\n\d+\n', '\n', text)
        
        # Ensure sentences start with capital letters after periods
        text = re.sub(r'\.([a-z])', lambda m: '.' + ' ' + m.group(1).upper(), text)
        
        return text.strip()
    
    def extract_images_from_page(self, page, page_num: int, output_dir: str) -> List[Tuple[str, str]]:
        """Extract images from a PDF page and return list of (filename, ocr_text) tuples"""
        image_results = []
        image_list = page.get_images(full=True)
        
        for img_index, img in enumerate(image_list):
            xref = img[0]
            pix = None
            try:
                pix = fitz.Pixmap(page.parent, xref)
                
                # Handle different colorspaces
                filename = f"page_{page_num}_image_{img_index + 1}.png"
                filepath = os.path.join(output_dir, filename)
                
                # Check if we need to convert colorspace
                final_pix = None
                conversion_needed = False
                
                # Handle different colorspaces
                channels = pix.n - pix.alpha
                
                # Check if pixmap is compatible with PNG (must be true grayscale or RGB)
                # We need to check the actual colorspace, not just channel count
                colorspace_str = str(pix.colorspace) if pix.colorspace else "None"
                
                if pix.colorspace and pix.colorspace == fitz.csGRAY and channels == 1:
                    # True grayscale image - save directly
                    final_pix = pix
                elif pix.colorspace and pix.colorspace == fitz.csRGB and channels == 3:
                    # RGB image - save directly
                    final_pix = pix
                else:
                    # Any other colorspace (CMYK, DeviceN, etc.) needs conversion
                    conversion_needed = True
                    try:
                        # Convert to RGB
                        final_pix = fitz.Pixmap(fitz.csRGB, pix)
                        print(f"Converted image to RGB: {filename}")
                    except Exception as conv_error:
                        print(f"Warning: Could not convert image {filename}: {conv_error}")
                        error_filename = f"page_{page_num}_image_{img_index + 1}_ERROR.txt"
                        error_filepath = os.path.join(output_dir, error_filename)
                        with open(error_filepath, 'w') as f:
                            f.write(f"ERROR: Failed to convert image with colorspace {colorspace_str} - {conv_error}")
                        image_results.append((error_filename, ""))
                        continue
                
                # Extract OCR text from image if enabled
                ocr_text = ""
                if self.use_ocr and final_pix:
                    try:
                        img_data = final_pix.tobytes("png")
                        ocr_text = self.extract_text_from_image_ocr(img_data)
                        if ocr_text.strip():
                            print(f"✓ OCR extracted {len(ocr_text)} characters from {filename}")
                    except Exception as ocr_error:
                        print(f"Warning: OCR failed for {filename}: {ocr_error}")
                
                # Only save if we have a valid pixmap
                if final_pix:
                    try:
                        final_pix.save(filepath)
                        image_results.append((filename, ocr_text))
                    except Exception as save_error:
                        print(f"Warning: Could not save image {filename}: {save_error}")
                        error_filename = f"page_{page_num}_image_{img_index + 1}_ERROR.txt"
                        error_filepath = os.path.join(output_dir, error_filename)
                        with open(error_filepath, 'w') as f:
                            f.write(f"ERROR: Failed to save image - {save_error}")
                        image_results.append((error_filename, ""))
                    finally:
                        # Clean up converted pixmap if it was created
                        if conversion_needed and final_pix != pix:
                            final_pix = None
                
            except Exception as pix_error:
                print(f"Warning: Could not process image {img_index + 1} on page {page_num}: {pix_error}")
                error_filename = f"page_{page_num}_image_{img_index + 1}_ERROR.txt"
                error_filepath = os.path.join(output_dir, error_filename)
                with open(error_filepath, 'w') as f:
                    f.write(f"ERROR: Failed to process image - {pix_error}")
                image_results.append((error_filename, ""))
            finally:
                if pix:
                    pix = None
        
        return image_results
    
    def extract_text_with_image_positions(self, pdf_path: str, output_dir: str) -> str:
        """Extract text from PDF and insert image filenames at appropriate positions, with OCR support"""
        doc = fitz.open(pdf_path)
        full_text = ""
        
        # Create images directory
        images_dir = os.path.join(output_dir, "extracted_images")
        os.makedirs(images_dir, exist_ok=True)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            
            # Add page separator
            full_text += f"--- Page {page_num + 1} ---\n"
            
            # Extract images first (now returns tuples with OCR text)
            image_results = self.extract_images_from_page(page, page_num + 1, images_dir)
            
            # Extract text using normal PDF extraction
            page_text = page.get_text()
            page_text = self.clean_extracted_text(page_text)
            
            # Check if this is a scanned page (little extractable text)
            is_scanned = self.is_page_mostly_images(page)
            
            # If it's a scanned page or we have very little text, try OCR on the entire page
            ocr_page_text = ""
            if self.use_ocr and (is_scanned or len(page_text.strip()) < 100):
                print(f"Page {page_num + 1} appears to be scanned, applying OCR...")
                ocr_page_text = self.extract_text_from_page_ocr(page)
                if len(ocr_page_text.strip()) > len(page_text.strip()):
                    print(f"✓ OCR produced better results for page {page_num + 1}")
                    page_text = ocr_page_text
                elif ocr_page_text.strip():
                    print(f"✓ Combined PDF text with OCR text for page {page_num + 1}")
                    page_text = f"{page_text}\n\n[OCR Text]:\n{ocr_page_text}"
            
            # Insert image references and OCR text
            if image_results:
                image_section = ""
                for filename, ocr_text in image_results:
                    image_section += f"[IMAGE: {filename}]"
                    if ocr_text.strip():
                        image_section += f"\n[OCR from {filename}]:\n{ocr_text}\n"
                    image_section += "\n"
                full_text += f"{image_section}\n"
            
            full_text += page_text + "\n\n"
        
        doc.close()
        return full_text
    
    def split_text_by_tokens(self, text: str, base_filename: str, output_dir: str) -> List[str]:
        """Split text into chunks of approximately max_tokens each"""
        lines = text.split('\n')
        chunks = []
        current_chunk = ""
        current_tokens = 0
        
        for line in lines:
            line_tokens = self.count_tokens(line + '\n')
            
            if current_tokens + line_tokens > self.max_tokens and current_chunk:
                # Save current chunk
                chunks.append(current_chunk.strip())
                current_chunk = line + '\n'
                current_tokens = line_tokens
            else:
                current_chunk += line + '\n'
                current_tokens += line_tokens
        
        # Add remaining chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        # Save chunks to files
        output_files = []
        for i, chunk in enumerate(chunks):
            if len(chunks) == 1:
                filename = f"{base_filename}.txt"
            else:
                filename = f"{base_filename}_part_{i + 1}.txt"
            
            filepath = os.path.join(output_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(chunk)
            
            output_files.append(filepath)
            print(f"Created: {filepath} ({self.count_tokens(chunk):,} tokens)")
        
        return output_files
    
    def process_pdf(self, pdf_path: str, output_dir: str = None) -> Dict[str, any]:
        """Main processing function"""
        pdf_path = Path(pdf_path)
        
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        if output_dir is None:
            output_dir = pdf_path.parent / f"{pdf_path.stem}_extracted"
        else:
            output_dir = Path(output_dir)
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"Processing: {pdf_path}")
        print(f"Output directory: {output_dir}")
        
        # Extract text with image positions
        full_text = self.extract_text_with_image_positions(str(pdf_path), str(output_dir))
        
        # Split into token-based chunks
        base_filename = pdf_path.stem
        output_files = self.split_text_by_tokens(full_text, base_filename, str(output_dir))
        
        # Count images
        images_dir = output_dir / "extracted_images"
        image_count = len(list(images_dir.glob("*.png"))) if images_dir.exists() else 0
        
        return {
            "pdf_path": str(pdf_path),
            "output_dir": str(output_dir),
            "text_files": output_files,
            "image_count": image_count,
            "total_tokens": self.count_tokens(full_text)
        }
    
    def extract_text_from_image_ocr(self, image_data: bytes) -> str:
        """Extract text from image data using OCR"""
        if not self.use_ocr:
            return ""
        
        try:
            # Convert image data to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Perform OCR
            extracted_text = pytesseract.image_to_string(
                image, 
                lang=self.ocr_language,
                config='--psm 1'  # Automatic page segmentation with OSD
            )
            
            # Clean extracted text
            return self.clean_extracted_text(extracted_text)
            
        except Exception as e:
            print(f"Warning: OCR failed on image: {e}")
            return ""
    
    def extract_text_from_page_ocr(self, page) -> str:
        """Extract text from entire page using OCR (for scanned documents)"""
        if not self.use_ocr:
            return ""
        
        try:
            # Render page as image with high DPI for better OCR
            mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better OCR accuracy
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to PIL Image
            img_data = pix.tobytes("png")
            image = Image.open(io.BytesIO(img_data))
            
            # Perform OCR
            extracted_text = pytesseract.image_to_string(
                image, 
                lang=self.ocr_language,
                config='--psm 1'  # Automatic page segmentation with OSD
            )
            
            pix = None  # Clean up
            
            # Clean and return extracted text
            return self.clean_extracted_text(extracted_text)
            
        except Exception as e:
            print(f"Warning: Page OCR failed: {e}")
            return ""
    
    def is_page_mostly_images(self, page, text_threshold: int = 50) -> bool:
        """Determine if a page is mostly images (likely scanned) based on text content"""
        try:
            page_text = page.get_text().strip()
            # If very little extractable text, likely a scanned page
            return len(page_text) < text_threshold
        except:
            return True  # If we can't extract text, assume it's image-based

def main():
    parser = argparse.ArgumentParser(description="Extract text and images from PDF with token splitting and OCR support")
    parser.add_argument("pdf_path", nargs='+', help="Path to PDF file(s) - supports multiple files and wildcards")
    parser.add_argument("-o", "--output", help="Output directory (default: {pdf_name}_extracted for each file)")
    parser.add_argument("-t", "--max-tokens", type=int, default=45000, 
                       help="Maximum tokens per output file (default: 45000)")
    parser.add_argument("-b", "--batch", action="store_true", 
                       help="Batch mode: put all files in single output directory")
    parser.add_argument("--ocr", action="store_true", 
                       help="Enable OCR for scanned documents (requires Tesseract)")
    parser.add_argument("--ocr-lang", default="eng", 
                       help="OCR language code (default: eng). Examples: vie (Vietnamese), eng+vie (multiple)")
    
    args = parser.parse_args()
    
    try:
        extractor = PDFExtractor(
            max_tokens=args.max_tokens, 
            use_ocr=args.ocr,
            ocr_language=args.ocr_lang
        )
        
        # Handle multiple PDF files
        pdf_files = []
        for path_pattern in args.pdf_path:
            # Expand wildcards
            expanded_paths = Path().glob(path_pattern) if '*' in path_pattern else [Path(path_pattern)]
            for path in expanded_paths:
                if path.is_file() and path.suffix.lower() == '.pdf':
                    pdf_files.append(path)
        
        if not pdf_files:
            print("No PDF files found!", file=sys.stderr)
            sys.exit(1)
        
        print(f"Processing {len(pdf_files)} PDF file(s)...")
        
        total_files = 0
        total_images = 0
        total_tokens = 0
        
        for i, pdf_path in enumerate(pdf_files, 1):
            print(f"\n[{i}/{len(pdf_files)}] Processing: {pdf_path.name}")
            
            # Determine output directory (same logic as single file)
            if args.output:
                output_dir = Path(args.output) / f"{pdf_path.stem}_extracted"
            else:
                output_dir = pdf_path.parent / f"{pdf_path.stem}_extracted"
            
            try:
                result = extractor.process_pdf(str(pdf_path), str(output_dir))
                
                total_files += len(result['text_files'])
                total_images += result['image_count']
                total_tokens += result['total_tokens']
                
                print(f"  ✓ Text files: {len(result['text_files'])}")
                print(f"  ✓ Images: {result['image_count']}")
                print(f"  ✓ Tokens: {result['total_tokens']:,}")
                
            except Exception as e:
                print(f"  ✗ Error: {e}", file=sys.stderr)
                continue
        
        print("\n" + "="*50)
        print("BATCH EXTRACTION COMPLETE")
        print("="*50)
        print(f"PDFs processed: {len(pdf_files)}")
        print(f"Total text files: {total_files}")
        print(f"Total images: {total_images}")
        print(f"Total tokens: {total_tokens:,}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()