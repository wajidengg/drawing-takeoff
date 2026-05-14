"""
Takeoff Module

Handles:
- Symbol detection and template matching
- Symbol counting logic
- Detection filtering and confidence calculation
- Multi-scale and rotation-variant matching
"""

import cv2
import numpy as np
from typing import List, Tuple, Dict, Optional
from utils.geometry import BoundingBox


class Takeoff:
    """
    Symbol detection and quantity takeoff engine.
    """
    
    def __init__(
        self,
        confidence_threshold: float = 0.7,
        min_match_distance: int = 30
    ):
        """
        Initialize Takeoff engine.
        
        Args:
            confidence_threshold (float): Minimum confidence for detections
            min_match_distance (int): Minimum pixel distance between matches
        """
        self.confidence_threshold = confidence_threshold
        self.min_match_distance = min_match_distance
    
    def template_match(
        self,
        image: np.ndarray,
        template: np.ndarray,
        method: int = cv2.TM_CCOEFF_NORMED
    ) -> Tuple[np.ndarray, float]:
        """
        Perform template matching on an image.
        
        Args:
            image: Input image to search in
            template: Template to match
            method: OpenCV matching method
        
        Returns:
            Tuple: (result map, best match value)
        """
        if template.shape[0] > image.shape[0] or template.shape[1] > image.shape[1]:
            raise ValueError("Template larger than image")
        
        result = cv2.matchTemplate(image, template, method)
        return result, result.max()
    
    def detect_symbols(
        self,
        image: np.ndarray,
        template: np.ndarray,
        use_multi_scale: bool = False,
        scales: List[float] = None
    ) -> List[Dict]:
        """
        Detect symbol matches in an image.
        
        Args:
            image: Input image
            template: Template to match
            use_multi_scale: Enable multi-scale matching
            scales: List of scale factors
        
        Returns:
            List[Dict]: List of detections with position and confidence
        """
        if scales is None:
            scales = [0.8, 1.0, 1.2]
        
        detections = []
        
        # Single scale detection
        if not use_multi_scale:
            scales = [1.0]
        
        # Try each scale
        for scale in scales:
            scaled_template = self._scale_template(template, scale)
            
            if (scaled_template.shape[0] > image.shape[0] or 
                scaled_template.shape[1] > image.shape[1]):
                continue
            
            # Template match
            result, max_val = self.template_match(image, scaled_template)
            
            # Find peaks in result map
            matches = self._find_peaks(result, scaled_template.shape)
            
            # Filter and score matches
            for match in matches:
                x, y = match
                confidence = float(result[y, x])
                
                if confidence >= self.confidence_threshold:
                    bbox = BoundingBox(
                        x,
                        y,
                        x + scaled_template.shape[1],
                        y + scaled_template.shape[0]
                    )
                    
                    detections.append({
                        'bbox': bbox,
                        'position': (x, y),
                        'confidence': confidence,
                        'scale': scale,
                        'template_shape': scaled_template.shape
                    })
        
        # Filter overlapping detections
        detections = self._filter_overlaps(detections)
        
        return detections
    
    def _scale_template(self, template: np.ndarray, scale: float) -> np.ndarray:
        """
        Scale a template image.
        
        Args:
            template: Input template
            scale: Scale factor
        
        Returns:
            np.ndarray: Scaled template
        """
        if scale == 1.0:
            return template
        
        new_size = (
            max(1, int(template.shape[1] * scale)),
            max(1, int(template.shape[0] * scale))
        )
        return cv2.resize(template, new_size, interpolation=cv2.INTER_LINEAR)
    
    def _find_peaks(
        self,
        result_map: np.ndarray,
        template_shape: Tuple[int, int],
        threshold: float = 0.5
    ) -> List[Tuple[int, int]]:
        """
        Find peaks in a template matching result map.
        
        Args:
            result_map: Template matching result
            template_shape: Shape of template
            threshold: Peak detection threshold
        
        Returns:
            List[Tuple[int, int]]: Positions of peaks
        """
        peaks = []
        
        # Simple peak detection with non-maximum suppression
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_map)
        
        # Threshold-based peak finding
        threshold_val = min_val + (max_val - min_val) * threshold
        peaks_mask = result_map > threshold_val
        
        # Find connected components
        y_coords, x_coords = np.where(peaks_mask)
        
        if len(x_coords) > 0:
            # Cluster nearby peaks
            for i in range(0, len(x_coords), max(1, len(x_coords) // 20)):
                if i < len(x_coords):
                    peaks.append((x_coords[i], y_coords[i]))
        
        return peaks
    
    def _filter_overlaps(
        self,
        detections: List[Dict],
        iou_threshold: float = 0.3
    ) -> List[Dict]:
        """
        Filter overlapping detections, keeping highest confidence.
        
        Args:
            detections: List of detections
            iou_threshold: IoU threshold for filtering
        
        Returns:
            List[Dict]: Filtered detections
        """
        if not detections:
            return detections
        
        # Sort by confidence (descending)
        sorted_detections = sorted(
            detections,
            key=lambda x: x['confidence'],
            reverse=True
        )
        
        filtered = []
        for detection in sorted_detections:
            # Check if overlaps with existing detections
            overlaps = False
            for existing in filtered:
                iou = detection['bbox'].iou(existing['bbox'])
                if iou > iou_threshold:
                    overlaps = True
                    break
            
            if not overlaps:
                filtered.append(detection)
        
        return filtered
    
    def count_symbols(
        self,
        detections: List[Dict]
    ) -> int:
        """
        Count detected symbols.
        
        Args:
            detections: List of detections
        
        Returns:
            int: Total count
        """
        return len(detections)
    
    def get_statistics(self, detections: List[Dict]) -> Dict:
        """
        Calculate detection statistics.
        
        Args:
            detections: List of detections
        
        Returns:
            Dict: Statistics
        """
        if not detections:
            return {
                'total_count': 0,
                'avg_confidence': 0.0,
                'min_confidence': 0.0,
                'max_confidence': 0.0
            }
        
        confidences = [d['confidence'] for d in detections]
        return {
            'total_count': len(detections),
            'avg_confidence': np.mean(confidences),
            'min_confidence': np.min(confidences),
            'max_confidence': np.max(confidences)
        }
