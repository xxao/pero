#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero
import numpy


class TestCase(unittest.TestCase):
    """Test case for power interpolator."""
    
    
    def test_pow(self):
        """Tests whether interpolator works with 2 exponent."""
        
        interpol = pero.PowInterpol(power=2)
        
        # test inside
        self.assertAlmostEqual(interpol.normalize(50, 0, 100), 0.25, 10)
        self.assertAlmostEqual(interpol.denormalize(0.25, 0, 100), 50, 10)
        
        # test left
        self.assertAlmostEqual(interpol.normalize(0.01, 1, 100), -0.0001, 10)
        self.assertAlmostEqual(interpol.denormalize(-0.0001, 1, 100), 0.01, 10)
        
        # test right
        self.assertAlmostEqual(interpol.normalize(1000, 0, 100), 100, 10)
        self.assertAlmostEqual(interpol.denormalize(100, 0, 100), 1000, 2)
    
    
    def test_sqrt(self):
        """Tests whether interpolator works with 1/2 exponent."""
        
        interpol = pero.PowInterpol(power=0.5)
        
        # test inside
        self.assertAlmostEqual(interpol.normalize(36, 0, 100), 0.6, 10)
        self.assertAlmostEqual(interpol.denormalize(0.6, 0, 100), 36, 10)
        
        # test left
        self.assertAlmostEqual(interpol.normalize(0.01, 1, 100), -0.1, 10)
        self.assertAlmostEqual(interpol.denormalize(-0.1, 1, 100), 0.01, 10)
        
        # test right
        self.assertAlmostEqual(interpol.normalize(256, 0, 100), 1.6, 10)
        self.assertAlmostEqual(interpol.denormalize(1.6, 0, 100), 256, 10)
    
    
    def test_arrays(self):
        """Tests whether interpolator works correctly with arrays."""
        
        interpol = pero.PowInterpol(power=0.5)
        
        data = [0, 36, 256]
        model = [0, 0.6, 1.6]
        
        numpy.testing.assert_almost_equal(list(interpol.normalize(numpy.array(data), 0, 100)), model, 10)
        numpy.testing.assert_almost_equal(list(interpol.denormalize(numpy.array(model), 0, 100)), data, 10)


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
