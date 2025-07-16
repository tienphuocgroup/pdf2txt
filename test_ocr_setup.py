#!/usr/bin/env python3
"""
Test script for PDF Extractor with OCR functionality
Tests various features including OCR capabilities
"""

import os
import sys
import tempfile
from pathlib import Path

# Add the current directory to Python path to import our module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pdf_extractor import PDFExtractor

def test_basic_functionality():
    """Test basic PDF extraction without OCR"""
    print("🧪 Testing basic PDF extraction...")
    
    try:
        extractor = PDFExtractor(max_tokens=10000, use_ocr=False)
        print("✅ PDFExtractor initialized successfully (no OCR)")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize PDFExtractor: {e}")
        return False

def test_ocr_availability():
    """Test if OCR functionality is available"""
    print("🧪 Testing OCR availability...")
    
    try:
        extractor = PDFExtractor(max_tokens=10000, use_ocr=True, ocr_language="eng")
        if extractor.use_ocr:
            print("✅ OCR functionality is available")
            return True
        else:
            print("⚠️  OCR was requested but is not available")
            return False
    except Exception as e:
        print(f"❌ Failed to initialize OCR: {e}")
        return False

def test_dependencies():
    """Test if all required dependencies are installed"""
    print("🧪 Testing dependencies...")
    
    dependencies = {
        'fitz': 'PyMuPDF',
        'tiktoken': 'tiktoken',
        'pytesseract': 'pytesseract (for OCR)',
        'PIL': 'Pillow (for image processing)'
    }
    
    all_good = True
    
    for module, name in dependencies.items():
        try:
            __import__(module)
            print(f"✅ {name} - Available")
        except ImportError:
            print(f"❌ {name} - Missing")
            all_good = False
    
    return all_good

def test_ocr_languages():
    """Test available OCR languages"""
    print("🧪 Testing OCR languages...")
    
    try:
        import pytesseract
        languages = pytesseract.get_languages()
        print(f"✅ Available OCR languages: {', '.join(languages)}")
        
        # Check for common languages
        common_langs = ['eng', 'vie', 'fra', 'deu', 'spa']
        available_common = [lang for lang in common_langs if lang in languages]
        
        if available_common:
            print(f"✅ Common languages available: {', '.join(available_common)}")
        else:
            print("⚠️  No common languages found beyond basic English")
        
        return True
    except Exception as e:
        print(f"❌ Could not get OCR languages: {e}")
        return False

def test_file_processing():
    """Test file processing capabilities"""
    print("🧪 Testing file processing capabilities...")
    
    try:
        # Create a minimal test setup
        with tempfile.TemporaryDirectory() as temp_dir:
            print(f"✅ Temporary directory created: {temp_dir}")
            
            # Test token counting
            extractor = PDFExtractor()
            test_text = "This is a test sentence for token counting."
            token_count = extractor.count_tokens(test_text)
            print(f"✅ Token counting works: '{test_text}' = {token_count} tokens")
            
            # Test text cleaning
            dirty_text = "This   has    extra   spaces\n\n\n\nand  newlines-\nbroken"
            clean_text = extractor.clean_extracted_text(dirty_text)
            print(f"✅ Text cleaning works")
            print(f"   Before: {repr(dirty_text)}")
            print(f"   After:  {repr(clean_text)}")
            
            return True
    except Exception as e:
        print(f"❌ File processing test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 PDF Extractor OCR Test Suite")
    print("=" * 50)
    
    tests = [
        ("Basic Functionality", test_basic_functionality),
        ("Dependencies Check", test_dependencies),
        ("OCR Availability", test_ocr_availability),
        ("OCR Languages", test_ocr_languages),
        ("File Processing", test_file_processing),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        results[test_name] = test_func()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your setup is ready.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        
        if not results.get("OCR Availability", False):
            print("\n💡 To enable OCR functionality:")
            print("   1. Install Tesseract OCR (see TESSERACT_SETUP.md)")
            print("   2. Install Python packages: pip install pytesseract Pillow")
            print("   3. Re-run this test")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
