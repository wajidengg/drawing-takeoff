"""
PDF Loader Module

Handles:
- PDF loading and page extraction
- Rendering PDF pages into images (RGB format)
- Text extraction for future OCR phases
- Metadata retrieval
"""

import fitz  # PyMuPDF
import numpy as np
from typing import Optional, Tuple


class PDFLoader:
    """
    Handles PDF document loading, page rendering, and metadata extraction.
    """
    
    def __init__(self, pdf_path: str, dpi: int = 150):
        """
        Initialize PDFLoader.
        
        Args:
            pdf_path (str): Path to the PDF file
            dpi (int): DPI for rendering (default 150)
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
            np.ndarray: RGB image array
        """
        if page_num < 0 or page_num >= self.page_count:
            raise ValueError(f"Page {page_num} out of range [0, {self.page_count - 1}]")
        
        # Get page
        page = self.document[page_num]
        
        # Render at specified DPI with zoom
        mat = fitz.Matrix(self.dpi / 72.0 * zoom, self.dpi / 72.0 * zoom)
        pix = page.get_pixmap(matrix=mat, alpha=False)
        
        # Convert to numpy array
        img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
        
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
        Close the PDF document.
        """
        self.document.close()
    
    def __del__(self):
        """
        Cleanup when object is destroyed.
        """
        try:
            self.close()
        except:
            pass
