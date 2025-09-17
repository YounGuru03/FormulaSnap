"""
Basic tests for FormulaSnap components
"""

import unittest
import sys
import os

# Add the parent directory to the path so we can import formulasnap
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from formulasnap.ocr_engine import FormulaOCR
from PIL import Image
import numpy as np


class TestFormulaOCR(unittest.TestCase):
    """Test cases for the OCR engine"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.ocr = FormulaOCR()
    
    def test_ocr_initialization(self):
        """Test that OCR engine initializes correctly"""
        self.assertIsInstance(self.ocr, FormulaOCR)
    
    def test_preprocess_image(self):
        """Test image preprocessing"""
        # Create a simple test image
        img_array = np.ones((100, 100, 3), dtype=np.uint8) * 255
        test_image = Image.fromarray(img_array)
        
        # Test preprocessing
        processed = self.ocr.preprocess_image(test_image)
        
        self.assertIsInstance(processed, Image.Image)
        self.assertIsNotNone(processed)
    
    def test_latex_conversion(self):
        """Test LaTeX conversion functionality"""
        # Create a simple test image
        img_array = np.ones((100, 100, 3), dtype=np.uint8) * 255
        test_image = Image.fromarray(img_array)
        
        # Test LaTeX extraction (will use fallback)
        latex_result = self.ocr.extract_formula_latex(test_image)
        
        # Should return something (even if fallback)
        self.assertIsNotNone(latex_result)
    
    def test_typst_conversion(self):
        """Test Typst conversion functionality"""
        # Test LaTeX to Typst conversion
        latex_input = r"\frac{x^2 + y^2}{z}"
        expected_typst = "frac(x^2 + y^2, z)"
        
        result = self.ocr._convert_latex_to_typst(latex_input)
        self.assertEqual(result, expected_typst)
    
    def test_model_ready_status(self):
        """Test model readiness check"""
        # This should return a boolean
        is_ready = self.ocr.is_model_ready()
        self.assertIsInstance(is_ready, bool)


class TestApplicationStructure(unittest.TestCase):
    """Test basic application structure"""
    
    def test_import_main_module(self):
        """Test that main module can be imported"""
        try:
            from formulasnap import main
            self.assertTrue(True)  # If we get here, import worked
        except ImportError as e:
            self.fail(f"Could not import main module: {e}")
    
    def test_import_gui_module(self):
        """Test that GUI module can be imported"""
        try:
            from formulasnap import gui
            self.assertTrue(True)  # If we get here, import worked
        except ImportError as e:
            self.fail(f"Could not import GUI module: {e}")
    
    def test_package_version(self):
        """Test that package has version information"""
        try:
            from formulasnap import __version__
            self.assertIsInstance(__version__, str)
            self.assertTrue(len(__version__) > 0)
        except ImportError:
            self.fail("Could not import version information")


if __name__ == '__main__':
    unittest.main()