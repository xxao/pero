#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero
import numpy


class TestCase(unittest.TestCase):
    """Test case for transformation Matrix class."""
    
    
    def test_init(self):
        """Tests affine coefficient order and default identity matrix."""
        
        matrix = pero.Matrix(2, 3, 5, 7, 11, 13)
        numpy.testing.assert_allclose(matrix.transform(17, 19), (140, 197))
        
        matrix = pero.Matrix(a=0.5, d=-0.25, tx=1.25, ty=-2.5)
        numpy.testing.assert_allclose(matrix.transform(4, 8), (3.25, -4.5))
        
        matrix = pero.Matrix()
        numpy.testing.assert_allclose(matrix.transform(17, 19), (17, 19))
    
    
    def test_invert(self):
        """Tests inverse mapping and independence of an inverted clone."""
        
        matrix = pero.Matrix().translate(11, -7).rotate(0.37).scale(-2, 0.5)
        points = ((0, 0), (1.5, -2.25), (1000, -1000))
        transformed = [matrix.transform(*point) for point in points]
        
        inverse = matrix.clone()
        self.assertIs(inverse.invert(), inverse)
        
        for point, mapped in zip(points, transformed):
            numpy.testing.assert_allclose(
                inverse.transform(*mapped), point, atol=1e-10)
            numpy.testing.assert_allclose(matrix.transform(*point), mapped)
        
        identity = pero.Matrix().invert()
        numpy.testing.assert_allclose(identity.transform(3, -4), (3, -4))
    
    
    def test_invert_singular(self):
        """Tests that a failed inversion leaves the matrix unchanged."""
        
        matrix = pero.Matrix(1, 2, 2, 4, 3, 5)
        before = matrix.transform(2.5, -1.5)
        
        with self.assertRaises(numpy.linalg.LinAlgError):
            matrix.invert()
        
        numpy.testing.assert_allclose(matrix.transform(2.5, -1.5), before)
    
    
    def test_transform_arrays(self):
        """Tests paired arrays, broadcasting and empty coordinates."""
        
        matrix = pero.Matrix(2, 3, 5, 7, 11, 13)
        numpy.testing.assert_allclose(
            matrix.transform([1, 2], [3, 4]), ((28, 35), (37, 47)))
        numpy.testing.assert_allclose(
            matrix.transform([1, 2], 3), ((28, 30), (37, 40)))
        
        result = matrix.transform(
            numpy.array([[1], [2]]), numpy.array([[3, 4, 5]]))
        self.assertEqual(result.shape, (2, 2, 3))
        numpy.testing.assert_allclose(result, (
            ((28, 33, 38), (30, 35, 40)),
            ((37, 44, 51), (40, 47, 54))))
        self.assertEqual(matrix.transform([], []).shape, (2, 0))
    
    
    def test_transform_array_inverse(self):
        """Tests inverse mapping of multidimensional coordinate arrays."""
        
        matrix = pero.Matrix(2, 3, 5, 7, 11, 13)
        x = numpy.array([[0.2, -3], [4, 0]])
        y = numpy.array([[0.5, 2], [7, -1]])
        tx, ty = matrix.transform(x, y)
        result = matrix.clone().invert().transform(tx, ty)
        numpy.testing.assert_allclose(result, (x, y), atol=1e-10)
    
    
    def test_transform_incompatible_shapes(self):
        """Tests rejection of coordinate shapes that cannot broadcast."""
        
        with self.assertRaises(ValueError):
            pero.Matrix().transform([1, 2], [3, 4, 5])
    
    
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
