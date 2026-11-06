#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero
import numpy


class TestCase(unittest.TestCase):
    """Test case for symmetric logarithmic interpolator."""
    
    
    def test_linear_region(self):
        """Tests whether interpolator works correctly within linear region."""
        
        interpol = pero.SymlogInterpol(threshold=2)
        
        self.assertAlmostEqual(interpol.normalize(-2, -2, 2), 0, 10)
        self.assertAlmostEqual(interpol.denormalize(0, -2, 2), -2, 10)
        
        self.assertAlmostEqual(interpol.normalize(-1, -2, 2), 0.25, 10)
        self.assertAlmostEqual(interpol.denormalize(0.25, -2, 2), -1, 10)
        
        self.assertAlmostEqual(interpol.normalize(0, -2, 2), 0.5, 10)
        self.assertAlmostEqual(interpol.denormalize(0.5, -2, 2), 0, 10)
        
        self.assertAlmostEqual(interpol.normalize(1, -2, 2), 0.75, 10)
        self.assertAlmostEqual(interpol.denormalize(0.75, -2, 2), 1, 10)
        
        self.assertAlmostEqual(interpol.normalize(2, -2, 2), 1, 10)
        self.assertAlmostEqual(interpol.denormalize(1, -2, 2), 2, 10)
    
    
    def test_log_region(self):
        """Tests whether interpolator works correctly within logarithmic region."""
        
        interpol = pero.SymlogInterpol()
        
        self.assertAlmostEqual(interpol.normalize(-numpy.e, -1, 0), -1, 10)
        self.assertAlmostEqual(interpol.denormalize(-1, -1, 0), -numpy.e, 10)
        
        self.assertAlmostEqual(interpol.normalize(-1, -1, 0), 0, 10)
        self.assertAlmostEqual(interpol.denormalize(0, -1, 0), -1, 10)
        
        self.assertAlmostEqual(interpol.normalize(0, -1, 0), 1, 10)
        self.assertAlmostEqual(interpol.denormalize(1, -1, 0), 0, 10)
        
        self.assertAlmostEqual(interpol.normalize(1, -1, 0), 2, 10)
        self.assertAlmostEqual(interpol.denormalize(2, -1, 0), 1, 10)
        
        self.assertAlmostEqual(interpol.normalize(numpy.e, -1, 0), 3, 10)
        self.assertAlmostEqual(interpol.denormalize(3, -1, 0), numpy.e, 10)
    
    
    def test_arrays(self):
        """Tests whether interpolator works correctly with arrays."""
        
        interpol = pero.SymlogInterpol(threshold=2)
        
        data = [-2, -1, 0, 1, 2]
        model = [0, 0.25, 0.5, 0.75, 1]
        
        numpy.testing.assert_almost_equal(list(interpol.normalize(numpy.array(data), -2, 2)), model, 10)
        numpy.testing.assert_almost_equal(list(interpol.denormalize(numpy.array(model), -2, 2)), data, 10)
    
    
    def test_arrays_round_trip(self):
        """Tests whether array conversion is reversible for different ranges."""
        
        data = [-100, -2, -1, 0, 1, 2, 100]
        
        for threshold in (0.1, 1, 2, 10):
            interpol = pero.SymlogInterpol(threshold=threshold)
            
            model = interpol.normalize(numpy.array(data), -100, 100)
            numpy.testing.assert_almost_equal(list(interpol.denormalize(model, -100, 100)), data, 10)
            self.assertAlmostEqual(interpol.normalize(-100, -100, 100), 0, 10)
            self.assertAlmostEqual(interpol.normalize(100, -100, 100), 1, 10)
            
            model = interpol.normalize(numpy.array(data), 100, -100)
            numpy.testing.assert_almost_equal(list(interpol.denormalize(model, 100, -100)), data, 10)
            self.assertAlmostEqual(interpol.normalize(100, 100, -100), 0, 10)
            self.assertAlmostEqual(interpol.normalize(-100, 100, -100), 1, 10)
            
            model = interpol.normalize(numpy.array(data), 1, 100)
            numpy.testing.assert_almost_equal(list(interpol.denormalize(model, 1, 100)), data, 10)
            self.assertAlmostEqual(interpol.normalize(1, 1, 100), 0, 10)
            self.assertAlmostEqual(interpol.normalize(100, 1, 100), 1, 10)
            
            model = interpol.normalize(numpy.array(data), -100, -1)
            numpy.testing.assert_almost_equal(list(interpol.denormalize(model, -100, -1)), data, 10)
            self.assertAlmostEqual(interpol.normalize(-100, -100, -1), 0, 10)
            self.assertAlmostEqual(interpol.normalize(-1, -100, -1), 1, 10)
    
    
    def test_custom_threshold(self):
        """Tests whether interpolator works correctly with custom threshold."""
        
        interpol = pero.SymlogInterpol(threshold=2)
        
        self.assertAlmostEqual(interpol.normalize(2 * numpy.e, 0, 2), 2, 10)
        self.assertAlmostEqual(interpol.denormalize(2, 0, 2), 2 * numpy.e, 10)
    
    
    def test_threshold_boundaries(self):
        """Tests whether the slope is continuous at both threshold boundaries."""
        
        interpol = pero.SymlogInterpol(threshold=2)
        
        step = 1e-6
        
        value = interpol.normalize(-2, 0, 2)
        left = (value - interpol.normalize(-2 - step, 0, 2)) / step
        right = (interpol.normalize(-2 + step, 0, 2) - value) / step
        
        self.assertAlmostEqual(left, 0.5, 6)
        self.assertAlmostEqual(right, 0.5, 6)
        
        value = interpol.normalize(2, 0, 2)
        left = (value - interpol.normalize(2 - step, 0, 2)) / step
        right = (interpol.normalize(2 + step, 0, 2) - value) / step
        
        self.assertAlmostEqual(left, 0.5, 6)
        self.assertAlmostEqual(right, 0.5, 6)
    
    
    def test_threshold_change(self):
        """Tests whether an updated threshold changes the transformation."""
        
        interpol = pero.SymlogInterpol()
        
        self.assertAlmostEqual(interpol.normalize(1, 0, numpy.e), 0.5, 10)
        
        interpol.threshold = numpy.e
        
        self.assertAlmostEqual(interpol.normalize(1, 0, numpy.e), 1 / numpy.e, 10)
    
    
    def test_zero_without_warnings(self):
        """Tests that inactive logarithmic branches do not warn at zero."""
        
        interpol = pero.SymlogInterpol()
        
        with numpy.errstate(all='raise'):
            self.assertEqual(interpol.normalize(0, -1, 1), 0.5)
            self.assertEqual(interpol.denormalize(0.5, -1, 1), 0)


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
