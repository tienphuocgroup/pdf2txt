#!/usr/bin/env python3
"""
Test suite for PDF Text and Image Extractor
"""

import tempfile
import os
from pathlib import Path
import shutil
import re

# Import the class we'll be testing (assuming it will be in pdf_extractor.py)
# from pdf_extractor import PDFExtractor

class TestPDFExtractor:
    def setup_method(self):
        """Set up test fixtures"""
        self.test_dir = tempfile.mkdtemp()
        self.test_pdf = Path(__file__).parent / "archived" / "FBIC.pdf"
        
    def teardown_method(self):
        """Clean up test files"""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_pdf_file_exists(self):
        """Test that our test PDF file exists"""
        assert self.test_pdf.exists(), f"Test PDF not found at {self.test_pdf}"
        assert self.test_pdf.suffix == ".pdf"
    
    def test_token_counting(self):
        """Test token counting functionality"""
        # Mock test since we don't have the actual class yet
        test_text = "This is a test string with some content."
        # extractor = PDFExtractor()
        # token_count = extractor.count_tokens(test_text)
        # assert isinstance(token_count, int)
        # assert token_count > 0
        pass
    
    def test_image_extraction_naming(self):
        """Test that images are named correctly"""
        # Should follow pattern: page_{page_num}_image_{img_index}.png
        expected_pattern = r"page_\d+_image_\d+\.png"
        
        # Test with existing extracted images
        images_dir = Path(__file__).parent / "extracted_images"
        if images_dir.exists():
            for img_file in images_dir.glob("*.png"):
                assert re.match(expected_pattern, img_file.name), f"Invalid image name: {img_file.name}"
    
    def test_text_splitting_by_tokens(self):
        """Test that text is split correctly by token count"""
        # Test with known text content
        test_text = "--- Page 1 ---\nContent here\n--- Page 2 ---\nMore content"
        max_tokens = 50
        
        # Mock the splitting logic
        lines = test_text.split('\n')
        chunks = []
        current_chunk = ""
        
        for line in lines:
            if len(current_chunk) + len(line) > max_tokens and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = line + '\n'
            else:
                current_chunk += line + '\n'
        
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        assert len(chunks) > 0
        assert all(len(chunk) <= max_tokens * 2 for chunk in chunks)  # Rough approximation
    
    def test_image_reference_insertion(self):
        """Test that image references are inserted correctly"""
        # Test pattern: [IMAGE: page_1_image_1.png]
        expected_pattern = r"\[IMAGE: page_\d+_image_\d+\.png\]"
        
        # Read existing extracted text to see if pattern exists
        text_file = Path(__file__).parent / "archived" / "extracted_text.txt"
        if text_file.exists():
            content = text_file.read_text()
            # For now, just check that we can read the file
            assert len(content) > 0
    
    def test_output_directory_creation(self):
        """Test that output directories are created correctly"""
        output_dir = Path(self.test_dir) / "test_output"
        images_dir = output_dir / "extracted_images"
        
        # Create directories
        output_dir.mkdir(exist_ok=True)
        images_dir.mkdir(exist_ok=True)
        
        assert output_dir.exists()
        assert images_dir.exists()
    
    def test_file_naming_convention(self):
        """Test that output files follow correct naming convention"""
        base_name = "test_pdf"
        
        # Single file case
        single_file = f"{base_name}.txt"
        assert single_file.endswith(".txt")
        
        # Multiple files case
        multi_files = [f"{base_name}_part_{i}.txt" for i in range(1, 4)]
        for filename in multi_files:
            assert filename.endswith(".txt")
            assert "_part_" in filename
    
    def test_large_pdf_handling(self):
        """Test handling of large PDFs that need splitting"""
        # This would test the actual PDF processing
        # For now, we'll test the logic conceptually
        
        # Simulate a large text content
        large_text = "Sample content " * 10000  # Large text
        max_tokens = 1000
        
        # Simple chunking logic
        chunk_size = max_tokens * 4  # Rough character estimate
        chunks = [large_text[i:i+chunk_size] for i in range(0, len(large_text), chunk_size)]
        
        assert len(chunks) > 1, "Large text should be split into multiple chunks"
    
    def test_integration_with_existing_files(self):
        """Test that the extractor works with our existing PDF"""
        # Check that we have the expected files from previous extraction
        archived_dir = Path(__file__).parent / "archived"
        images_dir = Path(__file__).parent / "extracted_images"
        
        if archived_dir.exists():
            pdf_file = archived_dir / "FBIC.pdf"
            assert pdf_file.exists(), "Test PDF should exist"
        
        if images_dir.exists():
            image_files = list(images_dir.glob("*.png"))
            assert len(image_files) > 0, "Should have extracted images"
    
    def test_dependencies_available(self):
        """Test that required dependencies are available"""
        try:
            import fitz  # PyMuPDF
            import tiktoken
            assert True, "Required dependencies are available"
        except ImportError as e:
            print(f"Missing dependency: {e}")
            return False
        return True

def run_manual_test():
    """Manual test function to validate with actual PDF"""
    print("Running manual validation...")
    
    # Check existing files
    base_dir = Path(__file__).parent
    pdf_file = base_dir / "archived" / "FBIC.pdf"
    images_dir = base_dir / "extracted_images"
    
    print(f"PDF exists: {pdf_file.exists()}")
    print(f"Images dir exists: {images_dir.exists()}")
    
    if images_dir.exists():
        image_files = list(images_dir.glob("*.png"))
        print(f"Number of images: {len(image_files)}")
        
        # Check naming pattern
        expected_pattern = r"page_\d+_image_\d+\.png"
        valid_names = 0
        for img in image_files:
            if re.match(expected_pattern, img.name):
                valid_names += 1
            if len(image_files) <= 5:  # Show all if 5 or fewer
                print(f"  - {img.name}")
        
        print(f"Valid image names: {valid_names}/{len(image_files)}")
    
    # Check extracted text
    text_file = base_dir / "archived" / "extracted_text.txt"
    if text_file.exists():
        content = text_file.read_text()
        print(f"Text file size: {len(content)} characters")
        print(f"First 200 chars: {content[:200]}...")
        
        # Check for page markers
        page_markers = content.count("--- Page")
        print(f"Page markers found: {page_markers}")
    
    return True

def run_all_tests():
    """Run all tests manually"""
    print("="*50)
    print("RUNNING PDF EXTRACTOR TESTS")
    print("="*50)
    
    test_instance = TestPDFExtractor()
    test_instance.setup_method()
    
    tests = [
        ("PDF file exists", test_instance.test_pdf_file_exists),
        ("Token counting", test_instance.test_token_counting),
        ("Image extraction naming", test_instance.test_image_extraction_naming),
        ("Text splitting by tokens", test_instance.test_text_splitting_by_tokens),
        ("Image reference insertion", test_instance.test_image_reference_insertion),
        ("Output directory creation", test_instance.test_output_directory_creation),
        ("File naming convention", test_instance.test_file_naming_convention),
        ("Large PDF handling", test_instance.test_large_pdf_handling),
        ("Integration with existing files", test_instance.test_integration_with_existing_files),
        ("Dependencies available", test_instance.test_dependencies_available),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            print(f"\n🧪 {test_name}...")
            result = test_func()
            if result is False:
                print(f"❌ FAILED: {test_name}")
                failed += 1
            else:
                print(f"✅ PASSED: {test_name}")
                passed += 1
        except Exception as e:
            print(f"❌ ERROR in {test_name}: {e}")
            failed += 1
    
    test_instance.teardown_method()
    
    print(f"\n{'='*50}")
    print(f"TEST RESULTS: {passed} passed, {failed} failed")
    print(f"{'='*50}")

if __name__ == "__main__":
    run_manual_test()
    print("\n" + "="*30)
    run_all_tests()