#!/usr/bin/env python3
"""
PDF Text and Image Extractor - GUI Version
A user-friendly graphical interface for extracting text and images from PDF files.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
from pathlib import Path
import sys

# Import the main extractor class
from pdf_extractor import PDFExtractor

class PDFExtractorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Text & Image Extractor")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        # Variables
        self.selected_files = []
        self.output_directory = tk.StringVar()
        self.max_tokens = tk.IntVar(value=45000)
        self.use_ocr = tk.BooleanVar(value=False)
        self.ocr_language = tk.StringVar(value="eng")
        self.processing = False
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(4, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="PDF Text & Image Extractor", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection
        ttk.Label(main_frame, text="Select PDF files:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        file_frame.columnconfigure(0, weight=1)
        
        ttk.Button(file_frame, text="Browse Files", 
                  command=self.select_files).grid(row=0, column=0, sticky=tk.W)
        ttk.Button(file_frame, text="Clear", 
                  command=self.clear_files).grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # File list
        self.file_listbox = tk.Listbox(main_frame, height=4)
        self.file_listbox.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        
        # Output directory
        ttk.Label(main_frame, text="Output directory:").grid(row=3, column=0, sticky=tk.W, pady=5)
        
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=3, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        output_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(output_frame, textvariable=self.output_directory).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(output_frame, text="Browse", 
                  command=self.select_output_directory).grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N), pady=10)
        
        # Max tokens setting
        ttk.Label(settings_frame, text="Max tokens per file:").grid(row=0, column=0, sticky=tk.W)
        token_spinbox = ttk.Spinbox(settings_frame, from_=10000, to=100000, increment=5000, 
                                   textvariable=self.max_tokens, width=10)
        token_spinbox.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # OCR settings
        ocr_check = ttk.Checkbutton(settings_frame, text="Enable OCR for scanned documents", 
                                   variable=self.use_ocr, command=self.toggle_ocr_settings)
        ocr_check.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(10, 5))
        
        # OCR Language setting
        self.ocr_frame = ttk.Frame(settings_frame)
        self.ocr_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(self.ocr_frame, text="OCR Language:").grid(row=0, column=0, sticky=tk.W)
        self.ocr_combo = ttk.Combobox(self.ocr_frame, textvariable=self.ocr_language, 
                                     values=["eng", "vie", "fra", "deu", "spa", "eng+vie"], 
                                     width=15, state="readonly")
        self.ocr_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0))
        
        # Initially disable OCR settings
        self.toggle_ocr_settings()
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, 
                                           maximum=100, length=300)
        self.progress_bar.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # Status text
        self.status_text = scrolledtext.ScrolledText(main_frame, height=10, width=70)
        self.status_text.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        main_frame.rowconfigure(6, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=3, pady=10)
        
        self.extract_button = ttk.Button(button_frame, text="Extract PDFs", 
                                        command=self.start_extraction)
        self.extract_button.grid(row=0, column=0, padx=(0, 10))
        
        ttk.Button(button_frame, text="Clear Log", 
                  command=self.clear_log).grid(row=0, column=1, padx=(0, 10))
        
        ttk.Button(button_frame, text="Exit", 
                  command=self.root.quit).grid(row=0, column=2)
        
        # Add some initial text
        self.log_message("Ready to extract PDF files...")
        self.log_message("Select PDF files and click 'Extract PDFs' to begin.")
    
    def select_files(self):
        """Select PDF files to process"""
        files = filedialog.askopenfilenames(
            title="Select PDF Files",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        
        if files:
            self.selected_files = list(files)
            self.file_listbox.delete(0, tk.END)
            for file in self.selected_files:
                self.file_listbox.insert(tk.END, os.path.basename(file))
            
            # Auto-set output directory to first file's directory
            if not self.output_directory.get():
                first_file_dir = os.path.dirname(self.selected_files[0])
                self.output_directory.set(first_file_dir)
    
    def clear_files(self):
        """Clear selected files"""
        self.selected_files = []
        self.file_listbox.delete(0, tk.END)
    
    def select_output_directory(self):
        """Select output directory"""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_directory.set(directory)
    
    def log_message(self, message):
        """Add message to status log"""
        self.status_text.insert(tk.END, f"{message}\n")
        self.status_text.see(tk.END)
        self.root.update_idletasks()
    
    def clear_log(self):
        """Clear the status log"""
        self.status_text.delete(1.0, tk.END)
    
    def start_extraction(self):
        """Start the extraction process in a separate thread"""
        if not self.selected_files:
            messagebox.showerror("Error", "Please select at least one PDF file.")
            return
        
        if not self.output_directory.get():
            messagebox.showerror("Error", "Please select an output directory.")
            return
        
        if self.processing:
            messagebox.showwarning("Warning", "Extraction is already in progress.")
            return
        
        # Start extraction in background thread
        self.processing = True
        self.extract_button.config(state='disabled')
        self.progress_var.set(0)
        
        thread = threading.Thread(target=self.extract_files)
        thread.daemon = True
        thread.start()
    
    def extract_files(self):
        """Extract files (runs in background thread)"""
        try:
            extractor = PDFExtractor(
                max_tokens=self.max_tokens.get(),
                use_ocr=self.use_ocr.get(),
                ocr_language=self.ocr_language.get()
            )
            total_files = len(self.selected_files)
            
            if self.use_ocr.get():
                self.log_message(f"OCR enabled (language: {self.ocr_language.get()})")
            
            self.log_message(f"Starting extraction of {total_files} file(s)...")
            
            for i, pdf_path in enumerate(self.selected_files):
                progress = (i / total_files) * 100
                self.progress_var.set(progress)
                
                filename = os.path.basename(pdf_path)
                self.log_message(f"Processing: {filename}")
                
                try:
                    # Set output directory for this file
                    output_dir = os.path.join(self.output_directory.get(), 
                                            f"{Path(pdf_path).stem}_extracted")
                    
                    result = extractor.process_pdf(pdf_path, output_dir)
                    
                    self.log_message(f"✓ Completed: {filename}")
                    self.log_message(f"  - Text files: {len(result['text_files'])}")
                    self.log_message(f"  - Images: {result['image_count']}")
                    self.log_message(f"  - Total tokens: {result['total_tokens']:,}")
                    
                except Exception as e:
                    self.log_message(f"✗ Error processing {filename}: {str(e)}")
            
            self.progress_var.set(100)
            self.log_message("Extraction completed!")
            messagebox.showinfo("Success", f"Successfully processed {total_files} file(s)!")
            
        except Exception as e:
            self.log_message(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Extraction failed: {str(e)}")
        
        finally:
            self.processing = False
            self.extract_button.config(state='normal')
    
    def toggle_ocr_settings(self):
        """Enable/disable OCR settings based on checkbox"""
        if self.use_ocr.get():
            # Enable OCR settings
            for widget in self.ocr_frame.winfo_children():
                widget.config(state='normal')
        else:
            # Disable OCR settings
            for widget in self.ocr_frame.winfo_children():
                if hasattr(widget, 'config'):
                    widget.config(state='disabled')

def main():
    root = tk.Tk()
    app = PDFExtractorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()