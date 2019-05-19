#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero
import numpy


class TestCase(unittest.TestCase):
    """Test case for linear interpolator."""
    
    
    def test_log10(self):
        """Tests whether interpolator works for log10 range."""
        
        interpol = pero.LogInterpol()
        
        # test inside
        self.assertEqual(interpol.normalize(10, 1, 100), 0.5)
        self.assertEqual(interpol.denormalize(0.5, 1, 100), 10)
        
        # test left
        self.assertAlmostEqual(interpol.normalize(0.1, 1, 100), -0.5, 10)
        self.assertAlmostEqual(interpol.denormalize(-0.5, 1, 100), 0.1, 10)
        
        # test right
        self.assertAlmostEqual(interpol.normalize(1000, 1, 100), 1.5, 10)
        self.assertAlmostEqual(interpol.denormalize(1.5, 1, 100), 1000, 10)
    
    
    def test_log2(self):
        """Tests whether interpolator works for log2 range."""
        
        interpol = pero.LogInterpol()
        
        # test inside
        self.assertEqual(interpol.normalize(2, 1, 4), 0.5)
        self.assertEqual(interpol.denormalize(0.5, 1, 4), 2)
        
        # test left
        self.assertAlmostEqual(interpol.normalize(0.5, 1, 4), -0.5, 10)
        self.assertAlmostEqual(interpol.denormalize(-0.5, 1, 4), 0.5, 10)
        
        # test right
        self.assertAlmostEqual(interpol.normalize(8, 1, 4), 1.5, 10)
        self.assertAlmostEqual(interpol.denormalize(1.5, 1, 4), 8, 10)
    
    
    def test_arrays(self):
        """Tests whether interpolator works correctly with arrays."""
        
        interpol = pero.LogInterpol()
        
        data = [0.1, 10, 100, 1000]
        model = [-0.5, 0.5, 1, 1.5]
        
        numpy.testing.assert_almost_equal(list(interpol.normalize(numpy.array(data), 1, 100)), model, 10)
        numpy.testing.assert_almost_equal(list(interpol.denormalize(numpy.array(model), 1, 100)), data, 10)


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
