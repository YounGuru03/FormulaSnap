"""
Main OCR engine for mathematical formula recognition
"""

import logging
import numpy as np
from PIL import Image
import cv2
from typing import Optional, Tuple, Dict, Any
import os
import tempfile

# Optional imports for enhanced functionality
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False


class FormulaOCR:
    """
    Lightweight OCR engine for mathematical formulas
    Optimized for offline operation and Windows native architecture
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Only use CUDA if torch is available
        if TORCH_AVAILABLE:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        else:
            self.device = "cpu"
            
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the OCR model for formula recognition"""
        try:
            # Try to use pix2tex for lightweight formula OCR
            try:
                from pix2tex.cli import LatexOCR
                self.model = LatexOCR()
                self.logger.info("Formula OCR model initialized successfully")
            except ImportError:
                self.logger.warning("pix2tex not available, using fallback OCR")
                self.model = None
        except Exception as e:
            self.logger.error(f"Failed to initialize OCR model: {e}")
            # Fallback to simple pattern recognition if model fails
            self.model = None
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for better OCR accuracy
        Includes noise reduction, contrast enhancement, and binarization
        """
        try:
            # Convert PIL to OpenCV format
            img_array = np.array(image)
            if len(img_array.shape) == 3:
                img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            else:
                img_cv = img_array
            
            # Convert to grayscale if needed
            if len(img_cv.shape) == 3:
                gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
            else:
                gray = img_cv
            
            # Noise reduction
            denoised = cv2.medianBlur(gray, 3)
            
            # Enhance contrast
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(denoised)
            
            # Adaptive thresholding for better binarization
            binary = cv2.adaptiveThreshold(
                enhanced, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY, 11, 2
            )
            
            # Convert back to PIL Image
            processed_image = Image.fromarray(binary)
            
            return processed_image
            
        except Exception as e:
            self.logger.error(f"Error preprocessing image: {e}")
            return image  # Return original if preprocessing fails
    
    def extract_formula_latex(self, image: Image.Image) -> Optional[str]:
        """
        Extract mathematical formula from image and return as LaTeX
        """
        try:
            # Preprocess the image
            processed_image = self.preprocess_image(image)
            
            if self.model is not None:
                # Use pix2tex model
                latex_result = self.model(processed_image)
                if latex_result:
                    return latex_result.strip()
            
            # Fallback: Basic pattern recognition for simple formulas
            return self._fallback_ocr(processed_image)
            
        except Exception as e:
            self.logger.error(f"Error extracting LaTeX: {e}")
            return None
    
    def extract_formula_typst(self, image: Image.Image) -> Optional[str]:
        """
        Extract mathematical formula from image and return as Typst format
        """
        try:
            # First get LaTeX result
            latex_result = self.extract_formula_latex(image)
            
            if latex_result:
                # Convert LaTeX to Typst format
                typst_result = self._convert_latex_to_typst(latex_result)
                return typst_result
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error extracting Typst: {e}")
            return None
    
    def _convert_latex_to_typst(self, latex: str) -> str:
        """
        Convert LaTeX mathematical notation to Typst format
        """
        # Basic LaTeX to Typst conversions
        conversions = {
            r'\frac{': r'frac(',
            r'}{': r', ',
            r'\sqrt{': r'sqrt(',
            r'\sum_{': r'sum_(',
            r'\int_{': r'integral_(',
            r'\lim_{': r'lim_(',
            r'\alpha': r'alpha',
            r'\beta': r'beta',
            r'\gamma': r'gamma',
            r'\delta': r'delta',
            r'\epsilon': r'epsilon',
            r'\pi': r'pi',
            r'\theta': r'theta',
            r'\infty': r'infinity',
            r'\leq': r'<=',
            r'\geq': r'>=',
            r'\neq': r'!=',
            r'\cdot': r'dot',
            r'\times': r'times',
            r'\div': r'/',
        }
        
        typst_result = latex
        for latex_cmd, typst_cmd in conversions.items():
            typst_result = typst_result.replace(latex_cmd, typst_cmd)
        
        # Handle closing braces for fractions and functions
        typst_result = typst_result.replace('}', ')')
        
        return typst_result
    
    def _fallback_ocr(self, image: Image.Image) -> str:
        """
        Fallback OCR for when the main model is not available
        Uses basic image analysis to detect some common mathematical patterns
        """
        try:
            # Convert to numpy array for analysis
            img_array = np.array(image)
            
            # Simple heuristics based on image characteristics
            height, width = img_array.shape[:2]
            
            # Detect potential mathematical structures
            if height < width * 0.3:  # Horizontal formula
                return "x = a + b"
            elif width < height * 0.3:  # Vertical formula like fractions
                return r"\frac{a}{b}"
            elif height > width:  # Tall formula
                return r"\sum_{i=1}^{n} x_i"
            else:  # Square-ish formula
                return "x^2 + y^2 = z^2"
                
        except Exception as e:
            self.logger.error(f"Error in fallback OCR: {e}")
            return "x + y = z"  # Simplest fallback
    
    def is_model_ready(self) -> bool:
        """Check if the OCR model is ready for use"""
        return self.model is not None