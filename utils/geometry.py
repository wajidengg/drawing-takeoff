"""
Geometry Module

Handles:
- Bounding box calculations
- Intersection and overlap detection
- Geometric transformations
- Distance calculations
"""

import numpy as np
from typing import Tuple


class BoundingBox:
    """
    Represents a bounding box with geometric operations.
    """
    
    def __init__(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int
    ):
        """
        Initialize BoundingBox.
        
        Args:
            x1, y1: Top-left corner
            x2, y2: Bottom-right corner
        """
        self.x1 = min(x1, x2)
        self.y1 = min(y1, y2)
        self.x2 = max(x1, x2)
        self.y2 = max(y1, y2)
    
    @property
    def width(self) -> int:
        """Get bounding box width."""
        return self.x2 - self.x1
    
    @property
    def height(self) -> int:
        """Get bounding box height."""
        return self.y2 - self.y1
    
    @property
    def area(self) -> int:
        """Get bounding box area."""
        return self.width * self.height
    
    @property
    def center(self) -> Tuple[int, int]:
        """Get bounding box center."""
        return (
            (self.x1 + self.x2) // 2,
            (self.y1 + self.y2) // 2
        )
    
    def intersect(self, other: 'BoundingBox') -> 'BoundingBox':
        """
        Get intersection of two bounding boxes.
        
        Args:
            other: Other bounding box
        
        Returns:
            BoundingBox: Intersection region
        """
        x1 = max(self.x1, other.x1)
        y1 = max(self.y1, other.y1)
        x2 = min(self.x2, other.x2)
        y2 = min(self.y2, other.y2)
        
        if x2 < x1 or y2 < y1:
            return BoundingBox(0, 0, 0, 0)
        
        return BoundingBox(x1, y1, x2, y2)
    
    def union(self, other: 'BoundingBox') -> 'BoundingBox':
        """
        Get union of two bounding boxes.
        
        Args:
            other: Other bounding box
        
        Returns:
            BoundingBox: Bounding box containing both
        """
        return BoundingBox(
            min(self.x1, other.x1),
            min(self.y1, other.y1),
            max(self.x2, other.x2),
            max(self.y2, other.y2)
        )
    
    def iou(self, other: 'BoundingBox') -> float:
        """
        Calculate Intersection over Union (IoU).
        
        Args:
            other: Other bounding box
        
        Returns:
            float: IoU value (0-1)
        """
        intersection = self.intersect(other)
        union_box = self.union(other)
        
        if union_box.area == 0:
            return 0.0
        
        return intersection.area / union_box.area
    
    def distance_to(self, other: 'BoundingBox') -> float:
        """
        Calculate Euclidean distance between centers.
        
        Args:
            other: Other bounding box
        
        Returns:
            float: Distance
        """
        c1 = self.center
        c2 = other.center
        return np.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)
    
    def contains(self, x: int, y: int) -> bool:
        """
        Check if point is inside bounding box.
        
        Args:
            x, y: Point coordinates
        
        Returns:
            bool: True if inside
        """
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2
    
    def to_tuple(self) -> Tuple[int, int, int, int]:
        """
        Convert to tuple.
        
        Returns:
            Tuple: (x1, y1, x2, y2)
        """
        return (self.x1, self.y1, self.x2, self.y2)
    
    def __repr__(self) -> str:
        return f"BoundingBox({self.x1}, {self.y1}, {self.x2}, {self.y2})"


class GeometryUtils:
    """
    Geometry utility functions.
    """
    
    @staticmethod
    def distance(
        p1: Tuple[int, int],
        p2: Tuple[int, int]
    ) -> float:
        """
        Calculate Euclidean distance between two points.
        
        Args:
            p1, p2: Point coordinates
        
        Returns:
            float: Distance
        """
        return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
    @staticmethod
    def point_in_polygon(
        point: Tuple[int, int],
        polygon: np.ndarray
    ) -> bool:
        """
        Check if point is inside polygon.
        
        Args:
            point: Point coordinates
            polygon: Polygon vertices
        
        Returns:
            bool: True if inside
        """
        x, y = point
        n = len(polygon)
        inside = False
        
        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        
        return inside
