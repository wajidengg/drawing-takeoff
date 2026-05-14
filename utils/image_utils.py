"""
Image Utils Module

Handles:
- Image processing operations
- Resizing and cropping
- Thresholding and filtering
- Edge detection
- Color space conversions
"""

import cv2
import numpy as np
from typing import Tuple, Optional


class ImageProcessor:
    """
    Image processing utilities.
    """
    
    @staticmethod
    def resize(
        image: np.ndarray,
        width: Optional[int] = None,
        height: Optional[int] = None,
        maintain_aspect: bool = True
    ) -> np.ndarray:
        """
        Resize an image.
        
        Args:
            image: Input image
            width: Target width (None to auto)
            height: Target height (None to auto)
            maintain_aspect: Keep aspect ratio
        
        Returns:
            np.ndarray: Resized image
        """
        h, w = image.shape[:2]
        
        if maintain_aspect:
            if width and not height:
                height = int((width / w) * h)
            elif height and not width:
                width = int((height / h) * w)
        
        if width and height:
            return cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)
        
        return image
    
    @staticmethod
    def crop(
        image: np.ndarray,
        x1: int,
        y1: int,
        x2: int,
        y2: int
    ) -> np.ndarray:
        """
        Crop an image to a region.
        
        Args:
            image: Input image
            x1, y1: Top-left corner
            x2, y2: Bottom-right corner
        
        Returns:
            np.ndarray: Cropped image
        """
        return image[y1:y2, x1:x2]
    
    @staticmethod
    def threshold(
        image: np.ndarray,
        thresh: int = 128,
        method: int = cv2.THRESH_BINARY
    ) -> np.ndarray:
        """
        Apply thresholding to an image.
        
        Args:
            image: Input image
            thresh: Threshold value
            method: Thresholding method
        
        Returns:
            np.ndarray: Thresholded image
        """
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        _, result = cv2.threshold(image, thresh, 255, method)
        return result
    
    @staticmethod
    def blur(
        image: np.ndarray,
        kernel_size: int = 5
    ) -> np.ndarray:
        """
        Apply Gaussian blur to an image.
        
        Args:
            image: Input image
            kernel_size: Kernel size (must be odd)
        
        Returns:
            np.ndarray: Blurred image
        """
        if kernel_size % 2 == 0:
            kernel_size += 1
        
        return cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    
    @staticmethod
    def edge_detection(
        image: np.ndarray,
        method: str = 'canny',
        low_threshold: int = 50,
        high_threshold: int = 150
    ) -> np.ndarray:
        """
        Detect edges in an image.
        
        Args:
            image: Input image
            method: Detection method ('canny', 'sobel')
            low_threshold: Low threshold for Canny
            high_threshold: High threshold for Canny
        
        Returns:
            np.ndarray: Edge map
        """
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        if method == 'canny':
            return cv2.Canny(image, low_threshold, high_threshold)
        elif method == 'sobel':
            sobelx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
            return np.sqrt(sobelx**2 + sobely**2).astype(np.uint8)
        
        return image
    
    @staticmethod
    def grayscale(image: np.ndarray) -> np.ndarray:
        """
        Convert image to grayscale.
        
        Args:
            image: Input image
        
        Returns:
            np.ndarray: Grayscale image
        """
        if len(image.shape) == 2:
            return image
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    @staticmethod
    def normalize(
        image: np.ndarray,
        alpha: float = 0.0,
        beta: float = 1.0
    ) -> np.ndarray:
        """
        Normalize image pixel values.
        
        Args:
            image: Input image
            alpha: Lower bound
            beta: Upper bound
        
        Returns:
            np.ndarray: Normalized image
        """
        return cv2.normalize(image, None, alpha, beta, cv2.NORM_MINMAX).astype(np.float32)
