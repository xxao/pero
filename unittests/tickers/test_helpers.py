#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for ticker helpers."""
    
    
    def test_step_size(self):
        """Tests whether step size calculation works correctly."""
        
        step = pero.tickers.calc_step_size(3, 1, (5,3,2,1))
        self.assertEqual(step, 3)
        
        step = pero.tickers.calc_step_size(3, 2, (5,3,2,1))
        self.assertEqual(step, 2)
        
        step = pero.tickers.calc_step_size(3, 3, (5,3,2,1))
        self.assertEqual(step, 1)
        
        step = pero.tickers.calc_step_size(3, 4, (5,3,2,1))
        self.assertAlmostEqual(step, 1)
        
        step = pero.tickers.calc_step_size(3, 5, (5,3,2,1))
        self.assertAlmostEqual(step, 0.5)
        
        step = pero.tickers.calc_step_size(3, 6, (5,3,2,1))
        self.assertAlmostEqual(step, 0.5)
        
        step = pero.tickers.calc_step_size(3, 7, (5,3,2,1))
        self.assertAlmostEqual(step, 0.5)
        
        step = pero.tickers.calc_step_size(3, 8, (5,3,2,1))
        self.assertAlmostEqual(step, 0.3)
        
        step = pero.tickers.calc_step_size(3, 9, (5,3,2,1))
        self.assertAlmostEqual(step, 0.3)
        
        step = pero.tickers.calc_step_size(3, 10, (5,3,2,1))
        self.assertAlmostEqual(step, 0.3)
    
    
    def test_step_size_fractions(self):
        """Tests whether step size calculation works correctly."""
        
        step = pero.tickers.calc_step_size(.3, 1, (5,3,2,1))
        self.assertAlmostEqual(step, .3)
        
        step = pero.tickers.calc_step_size(.3, 2, (5,3,2,1))
        self.assertAlmostEqual(step, .2)
        
        step = pero.tickers.calc_step_size(.3, 3, (5,3,2,1))
        self.assertAlmostEqual(step, .1)
        
        step = pero.tickers.calc_step_size(.3, 4, (5,3,2,1))
        self.assertAlmostEqual(step, .1)
        
        step = pero.tickers.calc_step_size(.3, 5, (5,3,2,1))
        self.assertAlmostEqual(step, .05)
        
        step = pero.tickers.calc_step_size(.3, 6, (5,3,2,1))
        self.assertAlmostEqual(step, .05)
        
        step = pero.tickers.calc_step_size(.3, 7, (5,3,2,1))
        self.assertAlmostEqual(step, .05)
        
        step = pero.tickers.calc_step_size(.3, 8, (5,3,2,1))
        self.assertAlmostEqual(step, .03)
        
        step = pero.tickers.calc_step_size(.3, 9, (5,3,2,1))
        self.assertAlmostEqual(step, .03)
        
        step = pero.tickers.calc_step_size(.3, 10, (5,3,2,1))
        self.assertAlmostEqual(step, .03)
    
    
    def test_step_size_minor(self):
        """Tests whether step size calculation works correctly."""
        
        step = pero.tickers.calc_step_size(3, 1, (5,3,2,1), exact=True)
        self.assertEqual(step, 3)
        
        step = pero.tickers.calc_step_size(3, 2, (5,3,2,1), exact=True)
        self.assertEqual(step, 1)
        
        step = pero.tickers.calc_step_size(3, 3, (5,3,2,1), exact=True)
        self.assertEqual(step, 1)
        
        step = pero.tickers.calc_step_size(3, 4, (5,3,2,1), exact=True)
        self.assertAlmostEqual(step, 1)
        
        step = pero.tickers.calc_step_size(3, 5, (5,3,2,1), exact=True)
        self.assertAlmostEqual(step, 0.5)
        
        step = pero.tickers.calc_step_size(3, 6, (5,3,2,1), exact=True)
        self.assertAlmostEqual(step, 0.5)
        
        step = pero.tickers.calc_step_size(3, 7, (5,3,2,1), exact=True)
        self.assertAlmostEqual(step, 0.5)
        
        step = pero.tickers.calc_step_size(3, 8, (5,3,2,1), exact=True)
        self.assertAlmostEqual(step, 0.3)
        
        step = pero.tickers.calc_step_size(3, 9, (5,3,2,1), exact=True)
        self.assertAlmostEqual(step, 0.3)
        
        step = pero.tickers.calc_step_size(3, 10, (5,3,2,1), exact=True)
        self.assertAlmostEqual(step, 0.3)
    
    
    def test_step_size_minor_fractions(self):
        """Tests whether step size calculation works correctly."""
        
        step = pero.tickers.calc_step_size(.3, 1, (5,3,2,1), exact=True)
        self.assertAlmostEqual(step, .3)
        
        step = pero.tickers.calc_step_size(.3, 2, (5,3,2,1), exact=True)
        self.assertAlmostEqual(step, .1)
        
        step = pero.tickers.calc_step_size(.3, 3, (5,3,2,1), exact=True)
        self.assertAlmostEqual(step, .1)
        
        step = pero.tickers.calc_step_size(.3, 4, (5,3,2,1), exact=True)
        self.assertAlmostEqual(step, .1)
        
        step = pero.tickers.calc_step_size(.3, 5, (5,3,2,1), exact=True)
        self.assertAlmostEqual(step, .05)
        
        step = pero.tickers.calc_step_size(.3, 6, (5,3,2,1), exact=True)
        self.assertAlmostEqual(step, .05)
        
        step = pero.tickers.calc_step_size(.3, 7, (5,3,2,1), exact=True)
        self.assertAlmostEqual(step, .05)
        
        step = pero.tickers.calc_step_size(.3, 8, (5,3,2,1), exact=True)
        self.assertAlmostEqual(step, .03)
        
        step = pero.tickers.calc_step_size(.3, 9, (5,3,2,1), exact=True)
        self.assertAlmostEqual(step, .03)
        
        step = pero.tickers.calc_step_size(.3, 10, (5,3,2,1), exact=True)
        self.assertAlmostEqual(step, .03)
    
    
    def test_precision(self):
        """Tests precision for signed ticks, zero and small values."""
        
        cases = (
            ((), 1.0),
            ((0,), 1.0),
            ((-2, -1), 1.0),
            ((-0.25, 0, 0.25), 0.01),
            ((0.25, 0.25), 0.01),
            ((0.30000000000000004,), 0.1),
            ((5e-324,), 5e-324),
            ((-5e-324,), 5e-324),
            ((1.0, 1.0000000000000002), 1e-16),
        )
        
        for ticks, expected in cases:
            with self.subTest(ticks=ticks):
                self.assertEqual(pero.tickers.calc_precision(ticks), expected)
    
    
    def test_lin_ticks(self):
        """Tests whether linear ticks are calculated correctly."""
        
        # test basic
        ticks = pero.tickers.make_lin_ticks(0, 5, 1)
        model = (0, 1, 2, 3, 4, 5)
        self.assertEqual(ticks, model)
        
        # test start
        ticks = pero.tickers.make_lin_ticks(0.5, 5, 1)
        model = (1, 2, 3, 4, 5)
        self.assertEqual(ticks, model)
        
        # test end
        ticks = pero.tickers.make_lin_ticks(0, 5.5, 1)
        model = (0, 1, 2, 3, 4, 5)
        self.assertEqual(ticks, model)
        
        ticks = pero.tickers.make_lin_ticks(0, 0.3, 0.1)
        model = (0, 0.1, 0.2, 0.3)
        self.assertEqual(ticks, model)
        
        # test reversed range
        ticks = pero.tickers.make_lin_ticks(5.5, 0.5, 1)
        model = (5, 4, 3, 2, 1)
        self.assertEqual(ticks, model)
        
        ticks = pero.tickers.make_lin_ticks(0.3, 0, 0.1)
        model = (0.3, 0.2, 0.1, 0)
        self.assertEqual(ticks, model)
    
    
    def test_power_ticks(self):
        """Tests whether power ticks are calculated correctly."""
        
        # test basic
        ticks = pero.tickers.make_power_ticks(1, 1000, 10)
        model = (1, 10, 100, 1000)
        self.assertEqual(ticks, model)
        
        # test step
        ticks = pero.tickers.make_power_ticks(1, 1024, 2, 3)
        model = (1, 8, 64, 512)
        self.assertEqual(ticks, model)
        
        # test inner range
        ticks = pero.tickers.make_power_ticks(5, 5000, 10)
        model = (10, 100, 1000)
        self.assertEqual(ticks, model)
        
        # test reversed range
        ticks = pero.tickers.make_power_ticks(5000, 5, 10)
        model = (1000, 100, 10)
        self.assertEqual(ticks, model)
    
    
    def test_extend_range(self):
        """Tests whether range is extended correctly."""
        
        self.assertEqual(pero.tickers.extend_range(0.5, 9.5, 2), (0, 10))
        self.assertEqual(pero.tickers.extend_range(2, 10, 2), (2, 10))
        self.assertEqual(pero.tickers.extend_range(-9.5, -0.5, 2), (-10, 0))
        self.assertEqual(pero.tickers.extend_range(9.5, 0.5, 2), (10, 0))
        self.assertEqual(pero.tickers.extend_range(0.15, 0.85, 0.1), (0.1, 0.9))
    
    
    def test_extend_log_range(self):
        """Tests whether log range is extended correctly."""
        
        self.assertEqual(pero.tickers.extend_log_range(5, 500, 10), (1, 1000))
        self.assertEqual(pero.tickers.extend_log_range(10, 1000, 10), (10, 1000))
        self.assertEqual(pero.tickers.extend_log_range(500, 5, 10), (1000, 1))
        self.assertEqual(pero.tickers.extend_log_range(0.9, 1100, 2), (0.5, 2048))


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
