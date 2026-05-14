"""
Render Module

Handles:
- Drawing visualization and overlays
- Bounding box rendering
- Text annotation
- Heatmap visualization
- Color utilities
"""

import cv2
import numpy as np
from typing import Tuple, List, Optional


class Renderer:
    """
    Visualization and rendering utilities for drawing analysis.
    """
    
    # Standard colors (BGR format for OpenCV)
    COLORS = {
        'red': (0, 0, 255),
        'green': (0, 255, 0),
        'blue': (255, 0, 0),
        'yellow': (0, 255, 255),
        'cyan': (255, 255, 0),
        'magenta': (255, 0, 255),
        'white': (255, 255, 255),
        'black': (0, 0, 0),
    }
    
    @staticmethod
    def draw_rectangle(
        image: np.ndarray,
        bbox: Tuple[int, int, int, int],
        color: str = 'green',
        thickness: int = 2,
        label: Optional[str] = None,
        label_color: str = 'white'
    ) -> np.ndarray:
        """
        Draw a rectangle on an image.
        
        Args:
            image: Input image
            bbox: Bounding box (x1, y1, x2, y2)
            color: Color name
            thickness: Line thickness
            label: Optional label text
            label_color: Label text color
        
        Returns:
            np.ndarray: Image with rectangle drawn
        """
        result = image.copy()
        x1, y1, x2, y2 = bbox
        bgr_color = Renderer.COLORS.get(color, Renderer.COLORS['green'])
        
        cv2.rectangle(result, (x1, y1), (x2, y2), bgr_color, thickness)
        
        if label:
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            font_thickness = 1
            label_color_bgr = Renderer.COLORS.get(label_color, Renderer.COLORS['white'])
            
            # Put text
            cv2.putText(
                result,
                label,
                (x1, y1 - 5),
                font,
                font_scale,
                label_color_bgr,
                font_thickness
            )
        
        return result
    
    @staticmethod
    def draw_rectangles(
        image: np.ndarray,
        bboxes: List[Tuple[int, int, int, int]],
        color: str = 'green',
        thickness: int = 2
    ) -> np.ndarray:
        """
        Draw multiple rectangles on an image.
        
        Args:
            image: Input image
            bboxes: List of bounding boxes
            color: Color name
            thickness: Line thickness
        
        Returns:
            np.ndarray: Image with rectangles drawn
        """
        result = image.copy()
        for bbox in bboxes:
            result = Renderer.draw_rectangle(result, bbox, color, thickness)
        return result
    
    @staticmethod
    def draw_text(
        image: np.ndarray,
        text: str,
        position: Tuple[int, int],
        color: str = 'white',
        font_scale: float = 0.6,
        thickness: int = 1
    ) -> np.ndarray:
        """
        Draw text on an image.
        
        Args:
            image: Input image
            text: Text to draw
            position: (x, y) position
            color: Color name
            font_scale: Font scale
            thickness: Text thickness
        
        Returns:
            np.ndarray: Image with text drawn
        """
        result = image.copy()
        font = cv2.FONT_HERSHEY_SIMPLEX
        bgr_color = Renderer.COLORS.get(color, Renderer.COLORS['white'])
        
        cv2.putText(
            result,
            text,
            position,
            font,
            font_scale,
            bgr_color,
            thickness
        )
        
        return result
    
    @staticmethod
    def create_heatmap(
        image: np.ndarray,
        matches: List[Tuple[int, int]],
        radius: int = 20,
        colormap: int = cv2.COLORMAP_JET
    ) -> np.ndarray:
        """
        Create a heatmap visualization of match locations.
        
        Args:
            image: Input image
            matches: List of (x, y) match positions
            radius: Radius of each heatmap point
            colormap: OpenCV colormap
        
        Returns:
            np.ndarray: Heatmap visualization
        """
        result = image.copy()
        heatmap = np.zeros((result.shape[0], result.shape[1]), dtype=np.float32)
        
        # Create Gaussian heatmap
        for x, y in matches:
            cv2.circle(heatmap, (x, y), radius, 1.0, -1)
        
        # Normalize
        if heatmap.max() > 0:
            heatmap = (heatmap / heatmap.max() * 255).astype(np.uint8)
        
        # Apply colormap
        heatmap_color = cv2.applyColorMap(heatmap, colormap)
        
        # Blend with original
        result = cv2.addWeighted(result, 0.7, heatmap_color, 0.3, 0)
        
        return result
    
    @staticmethod
    def overlay_legend_region(
        image: np.ndarray,
        legend_bbox: Tuple[int, int, int, int],
        opacity: float = 0.3
    ) -> np.ndarray:
        """
        Overlay legend region with semi-transparent color.
        
        Args:
            image: Input image
            legend_bbox: Bounding box of legend region
            opacity: Overlay opacity (0-1)
        
        Returns:
            np.ndarray: Image with legend overlay
        """
        result = image.copy()
        x1, y1, x2, y2 = legend_bbox
        
        overlay = result.copy()
        cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 255, 255), -1)  # Yellow
        
        cv2.addWeighted(overlay, opacity, result, 1 - opacity, 0, result)
        
        return result
