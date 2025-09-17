"""
Main GUI application for FormulaSnap
Windows-native interface using tkinter
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import pyperclip
import logging
import threading
import os
from typing import Optional
import io

from .ocr_engine import FormulaOCR


class FormulaSnapGUI:
    """
    Main GUI application for FormulaSnap
    Provides Windows-native interface for formula OCR
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("FormulaSnap - Math Formula OCR")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)
        
        # Set application icon and styling
        self.setup_styling()
        
        # Initialize OCR engine
        self.ocr_engine = FormulaOCR()
        
        # Current image and results
        self.current_image = None
        self.current_latex = None
        self.current_typst = None
        
        # Setup logging
        self.setup_logging()
        
        # Create GUI elements
        self.create_widgets()
        
        # Bind clipboard paste
        self.root.bind('<Control-v>', self.paste_from_clipboard)
        
        # Setup drag and drop (basic implementation)
        self.setup_drag_drop()
        
        self.logger.info("FormulaSnap GUI initialized")
    
    def setup_styling(self):
        """Setup Windows-native styling"""
        # Configure the style
        style = ttk.Style()
        
        # Use Windows native theme if available
        available_themes = style.theme_names()
        if 'vista' in available_themes:
            style.theme_use('vista')
        elif 'winnative' in available_themes:
            style.theme_use('winnative')
        
        # Set window icon
        try:
            # You can add an icon file later
            pass
        except Exception:
            pass
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def create_widgets(self):
        """Create and layout GUI widgets"""
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title label
        title_label = ttk.Label(
            main_frame, 
            text="FormulaSnap - Math Formula OCR", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Input", padding=10)
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Buttons for input
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X)
        
        self.paste_btn = ttk.Button(
            button_frame, 
            text="Paste from Clipboard (Ctrl+V)", 
            command=self.paste_from_clipboard
        )
        self.paste_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.open_btn = ttk.Button(
            button_frame, 
            text="Open Image File", 
            command=self.open_image_file
        )
        self.open_btn.pack(side=tk.LEFT)
        
        # Image display
        self.image_frame = ttk.Frame(input_frame)
        self.image_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.image_label = ttk.Label(
            self.image_frame, 
            text="No image loaded. Use Ctrl+V to paste or click 'Open Image File'",
            background="lightgray",
            anchor="center"
        )
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        # Process button
        self.process_btn = ttk.Button(
            main_frame,
            text="🔍 Extract Formula",
            command=self.process_image,
            state=tk.DISABLED
        )
        self.process_btn.pack(pady=10)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame, 
            mode='indeterminate'
        )
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding=10)
        results_frame.pack(fill=tk.BOTH, expand=True)
        
        # Notebook for LaTeX and Typst tabs
        self.notebook = ttk.Notebook(results_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # LaTeX tab
        latex_frame = ttk.Frame(self.notebook)
        self.notebook.add(latex_frame, text="LaTeX")
        
        latex_button_frame = ttk.Frame(latex_frame)
        latex_button_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(
            latex_button_frame,
            text="Copy LaTeX",
            command=self.copy_latex
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            latex_button_frame,
            text="Export LaTeX",
            command=self.export_latex
        ).pack(side=tk.LEFT)
        
        self.latex_text = scrolledtext.ScrolledText(
            latex_frame,
            wrap=tk.WORD,
            height=8,
            font=("Consolas", 10)
        )
        self.latex_text.pack(fill=tk.BOTH, expand=True)
        
        # Typst tab
        typst_frame = ttk.Frame(self.notebook)
        self.notebook.add(typst_frame, text="Typst")
        
        typst_button_frame = ttk.Frame(typst_frame)
        typst_button_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Button(
            typst_button_frame,
            text="Copy Typst",
            command=self.copy_typst
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            typst_button_frame,
            text="Export Typst",
            command=self.export_typst
        ).pack(side=tk.LEFT)
        
        self.typst_text = scrolledtext.ScrolledText(
            typst_frame,
            wrap=tk.WORD,
            height=8,
            font=("Consolas", 10)
        )
        self.typst_text.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(
            main_frame,
            textvariable=self.status_var,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def setup_drag_drop(self):
        """Setup basic drag and drop functionality"""
        # Note: For full drag-drop support, you might want to use tkinterdnd2
        # This is a simplified version
        def drop(event):
            try:
                # This is a basic implementation
                # In a full implementation, you'd parse the dropped files
                pass
            except Exception as e:
                self.logger.error(f"Error in drag-drop: {e}")
        
        self.image_label.bind("<Button-1>", drop)
    
    def paste_from_clipboard(self, event=None):
        """Paste image from clipboard"""
        try:
            from PIL import ImageGrab
            
            # Try to get image from clipboard
            image = ImageGrab.grabclipboard()
            
            if image is None:
                messagebox.showwarning(
                    "No Image", 
                    "No image found in clipboard. Copy an image first."
                )
                return
            
            self.load_image(image)
            self.status_var.set("Image pasted from clipboard")
            
        except Exception as e:
            self.logger.error(f"Error pasting from clipboard: {e}")
            messagebox.showerror(
                "Error", 
                f"Failed to paste from clipboard: {e}"
            )
    
    def open_image_file(self):
        """Open image file dialog"""
        try:
            file_path = filedialog.askopenfilename(
                title="Select Image File",
                filetypes=[
                    ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                    ("PNG files", "*.png"),
                    ("JPEG files", "*.jpg *.jpeg"),
                    ("All files", "*.*")
                ]
            )
            
            if file_path:
                image = Image.open(file_path)
                self.load_image(image)
                self.status_var.set(f"Loaded: {os.path.basename(file_path)}")
                
        except Exception as e:
            self.logger.error(f"Error opening image file: {e}")
            messagebox.showerror(
                "Error", 
                f"Failed to open image file: {e}"
            )
    
    def load_image(self, image: Image.Image):
        """Load image into the application"""
        try:
            self.current_image = image
            
            # Display image (resize for display)
            display_image = self.resize_for_display(image)
            photo = ImageTk.PhotoImage(display_image)
            
            self.image_label.configure(image=photo, text="")
            self.image_label.image = photo  # Keep a reference
            
            # Enable process button
            self.process_btn.configure(state=tk.NORMAL)
            
        except Exception as e:
            self.logger.error(f"Error loading image: {e}")
            messagebox.showerror("Error", f"Failed to load image: {e}")
    
    def resize_for_display(self, image: Image.Image, max_size=(400, 300)) -> Image.Image:
        """Resize image for display while maintaining aspect ratio"""
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        return image
    
    def process_image(self):
        """Process current image with OCR"""
        if self.current_image is None:
            messagebox.showwarning("No Image", "Please load an image first.")
            return
        
        # Start processing in a separate thread
        thread = threading.Thread(target=self._process_image_thread)
        thread.daemon = True
        thread.start()
    
    def _process_image_thread(self):
        """Process image in separate thread to avoid blocking UI"""
        try:
            # Update UI
            self.root.after(0, self._start_processing)
            
            # Extract formulas
            latex_result = self.ocr_engine.extract_formula_latex(self.current_image)
            typst_result = self.ocr_engine.extract_formula_typst(self.current_image)
            
            # Update UI with results
            self.root.after(0, self._finish_processing, latex_result, typst_result)
            
        except Exception as e:
            self.logger.error(f"Error processing image: {e}")
            self.root.after(0, self._processing_error, str(e))
    
    def _start_processing(self):
        """Update UI when processing starts"""
        self.process_btn.configure(state=tk.DISABLED)
        self.progress.start()
        self.status_var.set("Processing image...")
    
    def _finish_processing(self, latex_result: Optional[str], typst_result: Optional[str]):
        """Update UI when processing finishes"""
        self.progress.stop()
        self.process_btn.configure(state=tk.NORMAL)
        
        # Store results
        self.current_latex = latex_result
        self.current_typst = typst_result
        
        # Update text widgets
        self.latex_text.delete(1.0, tk.END)
        if latex_result:
            self.latex_text.insert(tk.END, latex_result)
        else:
            self.latex_text.insert(tk.END, "No LaTeX result generated")
        
        self.typst_text.delete(1.0, tk.END)
        if typst_result:
            self.typst_text.insert(tk.END, typst_result)
        else:
            self.typst_text.insert(tk.END, "No Typst result generated")
        
        self.status_var.set("Processing complete")
        
        # Show success message
        if latex_result or typst_result:
            messagebox.showinfo("Success", "Formula extraction completed!")
        else:
            messagebox.showwarning("No Results", "No formula could be extracted from the image.")
    
    def _processing_error(self, error_message: str):
        """Handle processing errors"""
        self.progress.stop()
        self.process_btn.configure(state=tk.NORMAL)
        self.status_var.set("Processing failed")
        messagebox.showerror("Processing Error", f"Failed to process image: {error_message}")
    
    def copy_latex(self):
        """Copy LaTeX result to clipboard"""
        if self.current_latex:
            pyperclip.copy(self.current_latex)
            self.status_var.set("LaTeX copied to clipboard")
            messagebox.showinfo("Copied", "LaTeX formula copied to clipboard!")
        else:
            messagebox.showwarning("No Data", "No LaTeX result to copy.")
    
    def copy_typst(self):
        """Copy Typst result to clipboard"""
        if self.current_typst:
            pyperclip.copy(self.current_typst)
            self.status_var.set("Typst copied to clipboard")
            messagebox.showinfo("Copied", "Typst formula copied to clipboard!")
        else:
            messagebox.showwarning("No Data", "No Typst result to copy.")
    
    def export_latex(self):
        """Export LaTeX result to file"""
        if not self.current_latex:
            messagebox.showwarning("No Data", "No LaTeX result to export.")
            return
        
        try:
            file_path = filedialog.asksaveasfilename(
                title="Export LaTeX",
                defaultextension=".tex",
                filetypes=[
                    ("LaTeX files", "*.tex"),
                    ("Text files", "*.txt"),
                    ("All files", "*.*")
                ]
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.current_latex)
                
                self.status_var.set(f"LaTeX exported to {os.path.basename(file_path)}")
                messagebox.showinfo("Exported", f"LaTeX exported to {file_path}")
                
        except Exception as e:
            self.logger.error(f"Error exporting LaTeX: {e}")
            messagebox.showerror("Error", f"Failed to export LaTeX: {e}")
    
    def export_typst(self):
        """Export Typst result to file"""
        if not self.current_typst:
            messagebox.showwarning("No Data", "No Typst result to export.")
            return
        
        try:
            file_path = filedialog.asksaveasfilename(
                title="Export Typst",
                defaultextension=".typ",
                filetypes=[
                    ("Typst files", "*.typ"),
                    ("Text files", "*.txt"),
                    ("All files", "*.*")
                ]
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.current_typst)
                
                self.status_var.set(f"Typst exported to {os.path.basename(file_path)}")
                messagebox.showinfo("Exported", f"Typst exported to {file_path}")
                
        except Exception as e:
            self.logger.error(f"Error exporting Typst: {e}")
            messagebox.showerror("Error", f"Failed to export Typst: {e}")
    
    def run(self):
        """Start the GUI application"""
        try:
            self.root.mainloop()
        except Exception as e:
            self.logger.error(f"Error running application: {e}")
            messagebox.showerror("Fatal Error", f"Application error: {e}")


def create_app() -> FormulaSnapGUI:
    """Factory function to create the application"""
    return FormulaSnapGUI()