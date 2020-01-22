#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero
import numpy


class TestCase(unittest.TestCase):
    """Test case for linear interpolator."""
    
    
    def test_positive(self):
        """Tests whether interpolator works correctly for positive range."""
        
        interpol = pero.LinInterpol()
        
        # test inside
        self.assertEqual(interpol.normalize(3, 2, 4), 0.5)
        self.assertEqual(interpol.denormalize(0.5, 2, 4), 3)
        
        # test left
        self.assertEqual(interpol.normalize(1, 2, 4), -0.5)
        self.assertEqual(interpol.denormalize(-0.5, 2, 4), 1)
        
        # test right
        self.assertEqual(interpol.normalize(5, 2, 4), 1.5)
        self.assertEqual(interpol.denormalize(1.5, 2, 4), 5)
        
        # test zero
        self.assertEqual(interpol.normalize(0, 2, 4), -1.0)
        self.assertEqual(interpol.denormalize(-1.0, 2, 4), 0)
    
    
    def test_positive_reversed(self):
        """Tests whether interpolator works correctly for positive reversed range."""
        
        interpol = pero.LinInterpol()
        
        # test inside
        self.assertEqual(interpol.normalize(3, 4, 2), 0.5)
        self.assertEqual(interpol.denormalize(0.5, 4, 2), 3)
        
        # test left
        self.assertEqual(interpol.normalize(5, 4, 2), -0.5)
        self.assertEqual(interpol.denormalize(-0.5, 4, 2), 5)
        
        # test right
        self.assertEqual(interpol.normalize(1, 4, 2), 1.5)
        self.assertEqual(interpol.denormalize(1.5, 4, 2), 1)
        
        # test zero
        self.assertEqual(interpol.normalize(0, 4, 2), 2.0)
        self.assertEqual(interpol.denormalize(2.0, 4, 2), 0)
    
    
    def test_negative(self):
        """Tests whether interpolator works correctly for negative range."""
        
        interpol = pero.LinInterpol()
        
        # test inside
        self.assertEqual(interpol.normalize(-3, -4, -2), 0.5)
        self.assertEqual(interpol.denormalize(0.5, -4, -2), -3)
        
        # test left
        self.assertEqual(interpol.normalize(-5, -4, -2), -0.5)
        self.assertEqual(interpol.denormalize(-0.5, -4, -2), -5)
        
        # test right
        self.assertEqual(interpol.normalize(-1, -4, -2), 1.5)
        self.assertEqual(interpol.denormalize(1.5, -4, -2), -1)
        
        # test zero
        self.assertEqual(interpol.normalize(0, -4, -2), 2.0)
        self.assertEqual(interpol.denormalize(2.0, -4, -2), 0)
    
    
    def test_negative_reversed(self):
        """Tests whether interpolator works correctly for negative reversed range."""
        
        interpol = pero.LinInterpol()
        
        # test inside
        self.assertEqual(interpol.normalize(-3, -2, -4), 0.5)
        self.assertEqual(interpol.denormalize(0.5, -2, -4), -3)
        
        # test left
        self.assertEqual(interpol.normalize(-1, -2, -4), -0.5)
        self.assertEqual(interpol.denormalize(-0.5, -2, -4), -1)
        
        # test right
        self.assertEqual(interpol.normalize(-5, -2, -4), 1.5)
        self.assertEqual(interpol.denormalize(1.5, -2, -4), -5)
        
        # test zero
        self.assertEqual(interpol.normalize(0, -2, -4), -1.0)
        self.assertEqual(interpol.denormalize(-1.0, -2, -4), 0)
    
    
    def test_zero_cross(self):
        """Tests whether interpolator works correctly for cross-zero range."""
        
        interpol = pero.LinInterpol()
        
        # test inside
        self.assertEqual(interpol.normalize(2, -2, 6), 0.5)
        self.assertEqual(interpol.denormalize(0.5, -2, 6), 2)
        
        # test left
        self.assertEqual(interpol.normalize(-4, -2, 6), -0.25)
        self.assertEqual(interpol.denormalize(-0.25, -2, 6), -4)
        
        # test right
        self.assertEqual(interpol.normalize(8, -2, 6), 1.25)
        self.assertEqual(interpol.denormalize(1.25, -2, 6), 8)
        
        # test zero
        self.assertEqual(interpol.normalize(0, -2, 6), 0.25)
        self.assertEqual(interpol.denormalize(0.25, -2, 6), 0)
    
    
    def test_zero_left(self):
        """Tests whether interpolator works correctly for left-zero range."""
        
        interpol = pero.LinInterpol()
        
        # test inside
        self.assertEqual(interpol.normalize(2, 0, 4), 0.5)
        self.assertEqual(interpol.denormalize(0.5, 0, 4), 2)
        
        # test left
        self.assertEqual(interpol.normalize(-2, 0, 4), -0.5)
        self.assertEqual(interpol.denormalize(-0.5, 0, 4), -2)
        
        # test right
        self.assertEqual(interpol.normalize(6, 0, 4), 1.5)
        self.assertEqual(interpol.denormalize(1.5, 0, 4), 6)
        
        # test zero
        self.assertEqual(interpol.normalize(0, 0, 4), 0)
        self.assertEqual(interpol.denormalize(0, 0, 4), 0)
    
    
    def test_zero_right(self):
        """Tests whether interpolator works correctly for right-zero range."""
        
        interpol = pero.LinInterpol()
        
        # test inside
        self.assertEqual(interpol.normalize(-2, -4, 0), 0.5)
        self.assertEqual(interpol.denormalize(0.5, -4, 0), -2)
        
        # test left
        self.assertEqual(interpol.normalize(-6, -4, 0), -0.5)
        self.assertEqual(interpol.denormalize(-0.5, -4, 0), -6)
        
        # test right
        self.assertEqual(interpol.normalize(2, -4, 0), 1.5)
        self.assertEqual(interpol.denormalize(1.5, -4, 0), 2)
        
        # test zero
        self.assertEqual(interpol.normalize(0, -4, 0), 1.0)
        self.assertEqual(interpol.denormalize(1.0, -4, 0), 0)
    
    
    def test_arrays(self):
        """Tests whether interpolator works correctly with arrays."""
        
        interpol = pero.LinInterpol()
        
        # test positive
        data = [0, 1, 3, 5]
        model = [-1., -0.5, 0.5, 1.5]
        
        self.assertEqual(list(interpol.normalize(numpy.array(data), 2, 4)), model)
        self.assertEqual(list(interpol.denormalize(numpy.array(model), 2, 4)), data)
        
        # test positive reversed
        data = [0, 1, 3, 5]
        model = [2., 1.5, 0.5, -0.5]
        
        self.assertEqual(list(interpol.normalize(numpy.array(data), 4, 2)), model)
        self.assertEqual(list(interpol.denormalize(numpy.array(model), 4, 2)), data)
        
        # test negative
        data = [0, -1, -3, -5]
        model = [2., 1.5, 0.5, -0.5]
        
        self.assertEqual(list(interpol.normalize(numpy.array(data), -4, -2)), model)
        self.assertEqual(list(interpol.denormalize(numpy.array(model), -4, -2)), data)
        
        # test negative reversed
        data = [0, -1, -3, -5]
        model = [-1., -0.5, 0.5, 1.5]
        
        self.assertEqual(list(interpol.normalize(numpy.array(data), -2, -4)), model)
        self.assertEqual(list(interpol.denormalize(numpy.array(model), -2, -4)), data)
        
        # test zero cross
        data = [-4, 0, 2, 8]
        model = [-0.25, 0.25, 0.5, 1.25]
        
        self.assertEqual(list(interpol.normalize(numpy.array(data), -2, 6)), model)
        self.assertEqual(list(interpol.denormalize(numpy.array(model), -2, 6)), data)
        
        # test zero left
        data = [-2, 0, 2, 6]
        model = [-0.5, 0, 0.5, 1.5]
        
        self.assertEqual(list(interpol.normalize(numpy.array(data), 0, 4)), model)
        self.assertEqual(list(interpol.denormalize(numpy.array(model), 0, 4)), data)
        
        # test zero right
        data = [-6, -2, 0, 2]
        model = [-0.5, 0.5, 1.0, 1.5]
        
        self.assertEqual(list(interpol.normalize(numpy.array(data), -4, 0)), model)
        self.assertEqual(list(interpol.denormalize(numpy.array(model), -4, 0)), data)


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
