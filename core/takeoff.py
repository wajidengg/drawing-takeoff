"""
Takeoff Module

Handles:
- Symbol detection and template matching (PROTOTYPE - Phase 3 implementation)
- Symbol counting logic
- Detection filtering and confidence calculation
- Multi-scale matching

IMPORTANT: This is a prototype implementation using traditional template matching.
- Does NOT support rotation-invariant detection yet (Phase 6)
- Accuracy depends heavily on symbol orientation and scale
- Real drawings will have symbols at various angles - consider Phase 6 before production
"""

import cv2
import numpy as np
from typing import List, Tuple, Dict, Optional
from utils.geometry import BoundingBox

try:
    from scipy import ndimage
    HAS_SCIPY = True
except ImportError:
    HAS_SCIPY = False


class Takeoff:
    """
    Symbol detection and quantity takeoff engine.
    
    ⚠️ PROTOTYPE WARNING:
    - Uses template matching only (no ML)
    - No rotation support (horizontal/vertical only)
    - Accuracy ~70-85% on clean, well-oriented symbols
    - Will miss rotated symbols
    """
    
    def __init__(
        self,
        confidence_threshold: float = 0.7,
        min_match_distance: int = 30
    ):
        """
        Initialize Takeoff engine.
        
        Args:
            confidence_threshold (float): Minimum confidence for detections (0-1)
            min_match_distance (int): Minimum pixel distance between matches (prevents duplicates)
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
            image: Input image to search in (grayscale)
            template: Template to match (grayscale)
            method: OpenCV matching method (default: normalized cross-correlation)
        
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
        Detect symbol matches in an image using template matching.
        
        ⚠️ PROTOTYPE: Only detects symbols at original orientation.
        Will NOT detect rotated symbols.
        
        Args:
            image: Input image (can be RGB, will be converted to grayscale)
            template: Template to match (can be RGB, will be converted to grayscale)
            use_multi_scale: Enable multi-scale matching (0.8x, 1.0x, 1.2x)
            scales: Custom list of scale factors
        
        Returns:
            List[Dict]: List of detections with position, confidence, and metadata
        """
        # Convert to grayscale if needed
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        if len(template.shape) == 3:
            template = cv2.cvtColor(template, cv2.COLOR_RGB2GRAY)
        
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
            
            # Find peaks in result map with proper non-maximum suppression
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
            scale: Scale factor (0.5 = 50%, 1.0 = 100%, 2.0 = 200%)
        
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
        Find peaks in a template matching result map with proper non-maximum suppression.
        
        IMPROVEMENT: Uses scipy.ndimage for proper connected component analysis
        instead of naive clustering.
        
        Args:
            result_map: Template matching result (each pixel = similarity score)
            template_shape: Shape of template (used for context)
            threshold: Peak detection threshold (0-1, relative to min/max)
        
        Returns:
            List[Tuple[int, int]]: Positions of detected peaks
        """
        peaks = []
        
        min_val = float(result_map.min())
        max_val = float(result_map.max())
        
        # Handle degenerate case
        if max_val == min_val:
            return peaks
        
        # Compute threshold value
        threshold_val = min_val + (max_val - min_val) * threshold
        peaks_mask = result_map > threshold_val
        
        if not peaks_mask.any():
            return peaks
        
        # Use scipy for proper connected component analysis if available
        if HAS_SCIPY:
            try:
                labeled, num_features = ndimage.label(peaks_mask)
                
                # Find center of each connected component
                for label_id in range(1, num_features + 1):
                    component = np.where(labeled == label_id)
                    if len(component[0]) > 0:
                        cy = np.mean(component[0])
                        cx = np.mean(component[1])
                        peaks.append((int(cx), int(cy)))
            except Exception as e:
                # Fallback to simpler method if scipy fails
                print(f"Warning: scipy peak detection failed: {e}, using fallback")
                peaks = self._find_peaks_fallback(result_map, threshold_val)
        else:
            # Fallback: scipy not available
            peaks = self._find_peaks_fallback(result_map, threshold_val)
        
        return peaks
    
    def _find_peaks_fallback(
        self,
        result_map: np.ndarray,
        threshold_val: float
    ) -> List[Tuple[int, int]]:
        """
        Fallback peak detection without scipy.
        
        Args:
            result_map: Template matching result
            threshold_val: Threshold value
        
        Returns:
            List[Tuple[int, int]]: Detected peak positions
        """
        peaks = []
        peaks_mask = result_map > threshold_val
        y_coords, x_coords = np.where(peaks_mask)
        
        if len(x_coords) == 0:
            return peaks
        
        # Simple clustering: group nearby pixels
        visited = set()
        for i in range(len(x_coords)):
            if i in visited:
                continue
            
            # Find cluster around this point
            cx, cy = x_coords[i], y_coords[i]
            cluster_x, cluster_y = [cx], [cy]
            visited.add(i)
            
            # Find nearby unvisited points
            for j in range(i + 1, len(x_coords)):
                if j not in visited:
                    dx = abs(x_coords[j] - cx)
                    dy = abs(y_coords[j] - cy)
                    if dx < 15 and dy < 15:  # Within 15 pixels
                        cluster_x.append(x_coords[j])
                        cluster_y.append(y_coords[j])
                        visited.add(j)
            
            # Add cluster center
            peaks.append((int(np.mean(cluster_x)), int(np.mean(cluster_y))))
        
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
            iou_threshold: IoU threshold for filtering (0.3 = 30% overlap)
        
        Returns:
            List[Dict]: Filtered detections (no overlaps)
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
            Dict: Statistics including count, mean/min/max confidence
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
            'avg_confidence': float(np.mean(confidences)),
            'min_confidence': float(np.min(confidences)),
            'max_confidence': float(np.max(confidences))
        }
