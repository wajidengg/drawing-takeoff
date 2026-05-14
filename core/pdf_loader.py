"""
PDF Loader Module

Handles:
- PDF loading and page extraction
- Rendering PDF pages into images (RGB format for Streamlit, BGR for OpenCV)
- Text extraction for future OCR phases
- Metadata retrieval
"""

import fitz  # PyMuPDF
import cv2
import numpy as np
from typing import Optional, Tuple


class PDFLoader:
    """
    Handles PDF document loading, page rendering, and metadata extraction.
    
    Note: Returns RGB images for Streamlit display. Convert to BGR/Grayscale
    for OpenCV operations in takeoff.py.
    """
    
    def __init__(self, pdf_path: str, dpi: int = 250):
        """
        Initialize PDFLoader.
        
        Args:
            pdf_path (str): Path to the PDF file
            dpi (int): DPI for rendering (default 250 - increased from 150 for better accuracy)
                       Higher DPI = better symbol detection but slower rendering
        """
        self.pdf_path = pdf_path
        self.dpi = dpi
        self.document = fitz.open(pdf_path)
        self.page_count = len(self.document)
    
    def render_page(self, page_num: int, zoom: float = 1.0) -> np.ndarray:
        """
        Render a PDF page to an RGB numpy array.
        
        Args:
            page_num (int): Page number (0-indexed)
            zoom (float): Zoom factor (default 1.0)
        
        Returns:
            np.ndarray: RGB image array (height, width, 3)
                       Ready for Streamlit display.
                       For OpenCV: convert to BGR or Grayscale.
        """
        if page_num < 0 or page_num >= self.page_count:
            raise ValueError(f"Page {page_num} out of range [0, {self.page_count - 1}]")
        
        # Get page
        page = self.document[page_num]
        
        # Render at specified DPI with zoom
        # DPI / 72.0 converts points to pixels
        mat = fitz.Matrix(self.dpi / 72.0 * zoom, self.dpi / 72.0 * zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        
        # Convert PyMuPDF pixmap to numpy array
        # PyMuPDF returns RGB (or RGBA), reshape to (height, width, channels)
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
            pix.height, pix.width, pix.n
        )
        
        # Handle RGBA → RGB conversion (drop alpha channel if present)
        if pix.n == 4:
            img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
        elif pix.n == 1:
            # Grayscale: expand to 3 channels for consistency
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        
        # At this point: img is RGB (height, width, 3)
        return img
    
    def extract_text(self, page_num: int) -> str:
        """
        Extract text from a PDF page.
        
        Args:
            page_num (int): Page number (0-indexed)
        
        Returns:
            str: Extracted text
        """
        if page_num < 0 or page_num >= self.page_count:
            raise ValueError(f"Page {page_num} out of range [0, {self.page_count - 1}]")
        
        page = self.document[page_num]
        return page.get_text()
    
    def get_page_dimensions(self, page_num: int) -> Tuple[int, int]:
        """
        Get page dimensions (width, height) in points.
        
        Args:
            page_num (int): Page number (0-indexed)
        
        Returns:
            Tuple[int, int]: (width, height)
        """
        if page_num < 0 or page_num >= self.page_count:
            raise ValueError(f"Page {page_num} out of range [0, {self.page_count - 1}]")
        
        page = self.document[page_num]
        rect = page.rect
        return (int(rect.width), int(rect.height))
    
    def close(self):
        """
        Close the PDF document and release resources.
        """
        if hasattr(self, 'document') and self.document:
            self.document.close()
    
    def __del__(self):
        """
        Cleanup when object is destroyed.
        """
        try:
            self.close()
        except Exception as e:
            print(f"Warning: Failed to close PDF: {e}")
