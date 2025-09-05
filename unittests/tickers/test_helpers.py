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
        self.assertAlmostEqual(step, 0.5)
        
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
        self.assertAlmostEqual(step, .05)
        
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
        self.assertAlmostEqual(step, 0.5)
        
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
        self.assertAlmostEqual(step, .05)
        
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
        
        # test reversed range
        ticks = pero.tickers.make_lin_ticks(5.5, 0.5, 1)
        model = (5, 4, 3, 2, 1)
        self.assertEqual(ticks, model)


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
