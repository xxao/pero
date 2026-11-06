#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero
import numpy


class TestCase(unittest.TestCase):
    """Test case for predefined square-root and symmetric logarithmic scales."""
    
    
    def test_sqrt(self):
        """Tests whether square-root scale works correctly."""
        
        scale = pero.SqrtScale(
            in_range = (0, 100),
            out_range = (10, 110))
        
        self.assertIsInstance(scale.normalizer, pero.SqrtInterpol)
        self.assertIsInstance(scale.converter, pero.LinInterpol)
        self.assertTrue(scale.is_property_locked('normalizer'))
        self.assertTrue(scale.is_property_locked('converter'))
        
        self.assertAlmostEqual(scale.scale(36), 70, 10)
        self.assertAlmostEqual(scale.invert(70), 36, 10)
        
        data = [0, 36, 100, 256]
        model = [10, 70, 110, 170]
        
        numpy.testing.assert_almost_equal(list(scale.scale(data)), model, 10)
        numpy.testing.assert_almost_equal(list(scale.invert(model)), data, 10)
    
    
    def test_symlog(self):
        """Tests whether symmetric logarithmic scale works correctly."""
        
        scale = pero.SymlogScale(
            in_range = (-2, 2),
            out_range = (0, 100),
            threshold = 2)
        
        self.assertIsInstance(scale.normalizer, pero.SymlogInterpol)
        self.assertIsInstance(scale.converter, pero.LinInterpol)
        self.assertTrue(scale.is_property_locked('normalizer'))
        self.assertTrue(scale.is_property_locked('converter'))
        self.assertEqual(scale.normalizer.threshold, 2)
        
        data = [-2, -1, 0, 1, 2]
        model = [0, 25, 50, 75, 100]
        
        numpy.testing.assert_almost_equal(list(scale.scale(data)), model, 10)
        numpy.testing.assert_almost_equal(list(scale.invert(model)), data, 10)
        
        self.assertAlmostEqual(scale.scale(2 * numpy.e), 150, 10)
        self.assertAlmostEqual(scale.invert(150), 2 * numpy.e, 10)
    
    
    def test_symlog_threshold(self):
        """Tests whether changing the threshold updates the scale."""
        
        scale = pero.SymlogScale(
            in_range = (0, numpy.e),
            out_range = (0, 100))
        
        self.assertAlmostEqual(scale.scale(1), 50, 10)
        
        scale.threshold = numpy.e
        
        self.assertEqual(scale.normalizer.threshold, numpy.e)
        self.assertAlmostEqual(scale.scale(1), 100 / numpy.e, 10)
        self.assertAlmostEqual(scale.invert(100 / numpy.e), 1, 10)
    
    
    def test_sqrt_reversed_clip(self):
        """Tests whether square-root scale supports reversed ranges and clipping."""
        
        scale = pero.SqrtScale(
            in_range = (100, 0),
            out_range = (110, 10),
            clip = True)
        
        data = [-1, 0, 36, 100, 256]
        model = [10, 10, 70, 110, 110]
        
        numpy.testing.assert_almost_equal(list(scale.scale(data)), model, 10)
        
        data = [0, 10, 70, 110, 170]
        model = [0, 0, 36, 100, 100]
        
        numpy.testing.assert_almost_equal(list(scale.invert(data)), model, 10)
    
    
    def test_symlog_reversed_clip(self):
        """Tests whether symmetric logarithmic scale supports clipping."""
        
        scale = pero.SymlogScale(
            in_range = (2, -2),
            out_range = (100, 0),
            threshold = 2,
            clip = True)
        
        data = [-10, -2, 0, 2, 10]
        model = [0, 0, 50, 100, 100]
        
        numpy.testing.assert_almost_equal(list(scale.scale(data)), model, 10)
        
        data = [-50, 0, 50, 100, 150]
        model = [-2, -2, 0, 2, 2]
        
        numpy.testing.assert_almost_equal(list(scale.invert(data)), model, 10)
    
    
    def test_gradient_sqrt(self):
        """Tests whether square-root gradient scale works correctly."""
        
        scale = pero.GradientSqrtScale(
            in_range = (0, 100),
            out_range = ('black', 'white'))
        
        self.assertIsInstance(scale.normalizer, pero.SqrtInterpol)
        self.assertTrue(scale.is_property_locked('normalizer'))
        
        model = scale.out_range.normalized(0, 1)
        
        self.assertEqual(scale.scale(36), model.color_at(0.6))
        self.assertEqual(scale.scale([0, 36, 100]), (model.color_at(0), model.color_at(0.6), model.color_at(1)))
    
    
    def test_gradient_symlog(self):
        """Tests whether symmetric logarithmic gradient scale works correctly."""
        
        scale = pero.GradientSymlogScale(
            in_range = (-2, 2),
            out_range = ('black', 'white'),
            threshold = 2)
        
        self.assertIsInstance(scale.normalizer, pero.SymlogInterpol)
        self.assertTrue(scale.is_property_locked('normalizer'))
        self.assertEqual(scale.normalizer.threshold, 2)
        
        model = scale.out_range.normalized(0, 1)
        
        self.assertEqual(scale.scale(1), model.color_at(0.75))
        self.assertEqual(scale.scale([-2, 0, 2]), (model.color_at(0), model.color_at(0.5), model.color_at(1)))
    
    
    def test_gradient_symlog_threshold(self):
        """Tests whether changing the threshold updates the gradient scale."""
        
        scale = pero.GradientSymlogScale(
            in_range = (0, numpy.e),
            out_range = ('black', 'white'))
        
        model = scale.out_range.normalized(0, 1)
        
        self.assertEqual(scale.scale(1), model.color_at(0.5))
        
        scale.threshold = numpy.e
        
        self.assertEqual(scale.normalizer.threshold, numpy.e)
        self.assertEqual(scale.scale(1), model.color_at(1 / numpy.e))


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
