"""
Basic Unit Tests for drawing-takeoff

Tests core functionality:
- Image processing
- Bounding box geometry
- PDF rendering
"""

import unittest
import numpy as np
from utils.image_utils import ImageProcessor
from utils.geometry import BoundingBox, GeometryUtils


class TestImageProcessor(unittest.TestCase):
    """
    Test ImageProcessor functionality.
    """
    
    def setUp(self):
        """Create test image."""
        self.image = np.ones((100, 100, 3), dtype=np.uint8) * 128
    
    def test_resize_width(self):
        """Test resize with width only."""
        resized = ImageProcessor.resize(self.image, width=50)
        self.assertEqual(resized.shape[1], 50)
    
    def test_resize_height(self):
        """Test resize with height only."""
        resized = ImageProcessor.resize(self.image, height=50)
        self.assertEqual(resized.shape[0], 50)
    
    def test_crop(self):
        """Test image cropping."""
        cropped = ImageProcessor.crop(self.image, 10, 10, 50, 50)
        self.assertEqual(cropped.shape, (40, 40, 3))
    
    def test_grayscale(self):
        """Test grayscale conversion."""
        gray = ImageProcessor.grayscale(self.image)
        self.assertEqual(len(gray.shape), 2)
    
    def test_blur(self):
        """Test Gaussian blur."""
        blurred = ImageProcessor.blur(self.image, kernel_size=5)
        self.assertEqual(blurred.shape, self.image.shape)


class TestBoundingBox(unittest.TestCase):
    """
    Test BoundingBox functionality.
    """
    
    def setUp(self):
        """Create test bounding boxes."""
        self.bbox1 = BoundingBox(0, 0, 10, 10)
        self.bbox2 = BoundingBox(5, 5, 15, 15)
    
    def test_width(self):
        """Test width calculation."""
        self.assertEqual(self.bbox1.width, 10)
    
    def test_height(self):
        """Test height calculation."""
        self.assertEqual(self.bbox1.height, 10)
    
    def test_area(self):
        """Test area calculation."""
        self.assertEqual(self.bbox1.area, 100)
    
    def test_center(self):
        """Test center calculation."""
        center = self.bbox1.center
        self.assertEqual(center, (5, 5))
    
    def test_iou(self):
        """Test Intersection over Union."""
        iou = self.bbox1.iou(self.bbox2)
        self.assertGreater(iou, 0)
        self.assertLess(iou, 1)
    
    def test_contains(self):
        """Test point containment."""
        self.assertTrue(self.bbox1.contains(5, 5))
        self.assertFalse(self.bbox1.contains(15, 15))
    
    def test_distance_to(self):
        """Test distance calculation."""
        distance = self.bbox1.distance_to(self.bbox2)
        self.assertGreater(distance, 0)


class TestGeometryUtils(unittest.TestCase):
    """
    Test GeometryUtils functionality.
    """
    
    def test_distance(self):
        """Test point distance calculation."""
        p1 = (0, 0)
        p2 = (3, 4)
        distance = GeometryUtils.distance(p1, p2)
        self.assertEqual(distance, 5.0)
    
    def test_distance_same_point(self):
        """Test distance between same points."""
        p = (5, 5)
        distance = GeometryUtils.distance(p, p)
        self.assertEqual(distance, 0.0)


if __name__ == '__main__':
    unittest.main()
