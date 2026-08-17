#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero
import numpy


class TestCase(unittest.TestCase):
    """Test case for transformation Matrix class."""
    
    
    def test_translate(self):
        """Tests whether points are translated correctly."""
        
        # translate positive
        matrix = pero.Matrix()
        matrix.translate(100, 200)
        x, y = matrix.transform(10, 20)
        
        self.assertEqual(x, 110)
        self.assertEqual(y, 220)
        
        # translate negative
        matrix = pero.Matrix()
        matrix.translate(-100, -200)
        x, y = matrix.transform(10, 20)
        
        self.assertEqual(x, -90)
        self.assertEqual(y, -180)
    
    
    def test_rotate(self):
        """Tests whether points are rotated correctly."""
        
        # rotate from zero
        matrix = pero.Matrix()
        matrix.rotate(numpy.pi*0.5)
        x, y = matrix.transform(10, 20)
        
        self.assertAlmostEqual(x, -20)
        self.assertAlmostEqual(y, 10)
        
        # rotate from origin
        matrix = pero.Matrix()
        matrix.rotate(numpy.pi*0.5, x=20, y=10)
        x, y = matrix.transform(10, 20)
        
        self.assertAlmostEqual(x, 10)
        self.assertAlmostEqual(y, 0)
        
        # rotate by degrees
        matrix = pero.Matrix()
        matrix.rotate(pero.rads(90))
        x, y = matrix.transform(10, 20)
        
        self.assertAlmostEqual(x, -20)
        self.assertAlmostEqual(y, 10)
        
        # rotate anticlockwise
        matrix = pero.Matrix()
        matrix.rotate(numpy.pi*0.5, clockwise=False)
        x, y = matrix.transform(10, 20)
        
        self.assertAlmostEqual(x, 20)
        self.assertAlmostEqual(y, -10)
    
    
    def test_scale(self):
        """Tests whether points are scaled correctly."""
        
        # scale up
        matrix = pero.Matrix()
        matrix.scale(2.5, 3)
        x, y = matrix.transform(10, 20)
        
        self.assertEqual(x, 25)
        self.assertEqual(y, 60)
        
        # scale down
        matrix = pero.Matrix()
        matrix.scale(.5, .2)
        x, y = matrix.transform(10, 20)
        
        self.assertEqual(x, 5)
        self.assertEqual(y, 4)
        
        # scale from origin
        matrix = pero.Matrix()
        matrix.scale(2, 3, x=20, y=10)
        x, y = matrix.transform(10, 20)
        
        self.assertEqual(x, 0)
        self.assertEqual(y, 40)
    
    
    def test_skew(self):
        """Tests whether points are skewed correctly."""
        
        # skew from zero
        matrix = pero.Matrix()
        matrix.skew(numpy.pi*0.25, numpy.pi*0.25)
        x, y = matrix.transform(10, 20)
        
        self.assertAlmostEqual(x, 30)
        self.assertAlmostEqual(y, 30)
        
        # skew from origin
        matrix = pero.Matrix()
        matrix.skew(numpy.pi*0.25, numpy.pi*0.25, x=20, y=10)
        x, y = matrix.transform(10, 20)
        
        self.assertAlmostEqual(x, 20)
        self.assertAlmostEqual(y, 10)
    
    
    def test_ray(self):
        """Tests whether points are rayed correctly."""
        
        # ray positive
        matrix = pero.Matrix()
        matrix.ray(10, numpy.pi/2)
        x, y = matrix.transform(10, 20)
        
        self.assertEqual(x, 10)
        self.assertEqual(y, 30)
        
        # ray negative
        matrix = pero.Matrix()
        matrix.ray(-10, numpy.pi/2)
        x, y = matrix.transform(10, 20)
        
        self.assertEqual(x, 10)
        self.assertEqual(y, 10)
    
    
    def test_hflip(self):
        """Tests whether points are flipped horizontally correctly."""
        
        # flip from zero
        matrix = pero.Matrix()
        matrix.hflip()
        x, y = matrix.transform(10, 20)
        
        self.assertEqual(x, -10)
        self.assertEqual(y, 20)
        
        # flip from origin
        matrix = pero.Matrix()
        matrix.hflip(5)
        x, y = matrix.transform(10, 20)
        
        self.assertEqual(x, 0)
        self.assertEqual(y, 20)
    
    
    def test_vflip(self):
        """Tests whether points are flipped vertically correctly."""
        
        # flip from zero
        matrix = pero.Matrix()
        matrix.vflip()
        x, y = matrix.transform(10, 20)
        
        self.assertEqual(x, 10)
        self.assertEqual(y, -20)
        
        # flip from origin
        matrix = pero.Matrix()
        matrix.vflip(10)
        x, y = matrix.transform(10, 20)
        
        self.assertEqual(x, 10)
        self.assertEqual(y, 0)


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
