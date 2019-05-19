#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for ticker helpers."""
    
    
    def test_step_size(self):
        """Tests whether step size calculation works correctly."""
        
        # test positive
        step = pero.tickers.step_size(10, 1, (5,3,2,1))
        self.assertEqual(step, 10)
        
        step = pero.tickers.step_size(10, 2, (5,3,2,1))
        self.assertEqual(step, 5)
        
        step = pero.tickers.step_size(10, 3, (5,3,2,1))
        self.assertEqual(step, 3)
        
        step = pero.tickers.step_size(10, 4, (5,3,2,1))
        self.assertEqual(step, 3)
        
        step = pero.tickers.step_size(10, 5, (5,3,2,1))
        self.assertEqual(step, 2)
        
        step = pero.tickers.step_size(10, 6, (5,3,2,1))
        self.assertEqual(step, 2)
        
        step = pero.tickers.step_size(10, 7, (5,3,2,1))
        self.assertEqual(step, 2)
        
        step = pero.tickers.step_size(10, 8, (5,3,2,1))
        self.assertEqual(step, 1)
        
        step = pero.tickers.step_size(10, 9, (5,3,2,1))
        self.assertEqual(step, 1)
        
        step = pero.tickers.step_size(10, 10, (5,3,2,1))
        self.assertEqual(step, 1)
    
    
    def test_ticks(self):
        """Tests whether linear ticks are calculated correctly."""
        
        # test basic
        ticks = pero.tickers.make_ticks(0, 5, 1)
        model = (0, 1, 2, 3, 4, 5)
        self.assertEqual(ticks, model)
        
        # test start
        ticks = pero.tickers.make_ticks(0.5, 5, 1)
        model = (1, 2, 3, 4, 5)
        self.assertEqual(ticks, model)
        
        # test end
        ticks = pero.tickers.make_ticks(0, 5.5, 1)
        model = (0, 1, 2, 3, 4, 5)
        self.assertEqual(ticks, model)
        
        # test reversed range
        ticks = pero.tickers.make_ticks(5.5, 0.5, 1)
        model = (5, 4, 3, 2, 1)
        self.assertEqual(ticks, model)


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
