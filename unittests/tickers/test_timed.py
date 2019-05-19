#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero
from numpy.testing import assert_array_almost_equal 


class TestCase(unittest.TestCase):
    """Test case for time ticker."""
    
    
    def test_major_ticks_hours(self):
        """Tests whether major ticks are calculated correctly for hours."""
        
        ticker = pero.TimeTicker()
        
        # step 10 hours
        ticker(start=0, end=50*3600, major_count=5)
        ticks = ticker.major_ticks()
        
        model = (0, 10*3600, 20*3600, 30*3600, 40*3600, 50*3600)
        self.assertEqual(ticks, model)
        
        # step 5 hours
        ticker(start=0, end=20*3600, major_count=5)
        ticks = ticker.major_ticks()
        
        model = (0, 5*3600, 10*3600, 15*3600, 20*3600)
        self.assertEqual(ticks, model)
        
        # step 2 hours
        ticker(start=0, end=10*3600, major_count=5)
        ticks = ticker.major_ticks()
        
        model = (0, 2*3600, 4*3600, 6*3600, 8*3600, 10*3600)
        self.assertEqual(ticks, model)
        
        # step 1 hour
        ticker(start=0, end=5*3600, major_count=5)
        ticks = ticker.major_ticks()
        
        model = (0, 1*3600, 2*3600, 3*3600, 4*3600, 5*3600)
        self.assertEqual(ticks, model)
        
        # step 30 min
        ticker(start=0, end=3*3600, major_count=7)
        ticks = ticker.major_ticks()
        
        model = (0, 30*60, 60*60, 90*60, 120*60, 150*60, 180*60)
        self.assertEqual(ticks, model)
        
        # step 15 min
        ticker(start=0, end=2*3600, major_count=7)
        ticks = ticker.major_ticks()
        
        model = (0, 15*60, 30*60, 45*60, 60*60, 75*60, 90*60, 105*60, 120*60)
        self.assertEqual(ticks, model)
        
        # step 10 min
        ticker(start=0, end=3600, major_count=7)
        ticks = ticker.major_ticks()
        
        model = (0, 10*60, 20*60, 30*60, 40*60, 50*60, 60*60)
        self.assertEqual(ticks, model)
    
    
    def test_major_ticks_minutes(self):
        """Tests whether major ticks are calculated correctly for minutes."""
        
        ticker = pero.TimeTicker()
        
        # step 15 min
        ticker(start=0, end=59*60, major_count=4)
        ticks = ticker.major_ticks()
        
        model = (0, 15*60, 30*60, 45*60)
        self.assertEqual(ticks, model)
        
        # step 10 min
        ticker(start=0, end=50*60, major_count=7)
        ticks = ticker.major_ticks()
        
        model = (0, 10*60, 20*60, 30*60, 40*60, 50*60)
        self.assertEqual(ticks, model)
        
        # step 5 min
        ticker(start=0, end=35*60, major_count=7)
        ticks = ticker.major_ticks()
        
        model = (0, 5*60, 10*60, 15*60, 20*60, 25*60, 30*60, 35*60)
        self.assertEqual(ticks, model)
        
        # step 2 min
        ticker(start=0, end=9*60, major_count=6)
        ticks = ticker.major_ticks()
        
        model = (0, 2*60, 4*60, 6*60, 8*60)
        self.assertEqual(ticks, model)
        
        # step 1 min
        ticker(start=0, end=7*60, major_count=7)
        ticks = ticker.major_ticks()
        
        model = (0, 1*60, 2*60, 3*60, 4*60, 5*60, 6*60, 7*60)
        self.assertEqual(ticks, model)
    
    
    def test_major_ticks_seconds(self):
        """Tests whether major ticks are calculated correctly for seconds."""
        
        ticker = pero.TimeTicker()
        
        # step 15 s
        ticker(start=0, end=59, major_count=4)
        ticks = ticker.major_ticks()
        
        model = (0, 15, 30, 45)
        self.assertEqual(ticks, model)
        
        # step 10 s
        ticker(start=0, end=50, major_count=7)
        ticks = ticker.major_ticks()
        
        model = (0, 10, 20, 30, 40, 50)
        self.assertEqual(ticks, model)
        
        # step 5 s
        ticker(start=0, end=35, major_count=7)
        ticks = ticker.major_ticks()
        
        model = (0, 5, 10, 15, 20, 25, 30, 35)
        self.assertEqual(ticks, model)
        
        # step 2 s
        ticker(start=0, end=9, major_count=6)
        ticks = ticker.major_ticks()
        
        model = (0, 2, 4, 6, 8)
        self.assertEqual(ticks, model)
        
        # step 1 s
        ticker(start=0, end=7, major_count=7)
        ticks = ticker.major_ticks()
        
        model = (0, 1, 2, 3, 4, 5, 6, 7)
        self.assertEqual(ticks, model)
    
    
    def test_major_ticks_milliseconds(self):
        """Tests whether major ticks are calculated correctly for milliseconds."""
        
        ticker = pero.TimeTicker()
        
        # step 0.5 s
        ticker(start=0, end=2, major_count=5)
        ticks = ticker.major_ticks()
        
        model = (0, 0.5, 1.0, 1.5, 2.0)
        self.assertEqual(ticks, model)
        
        # step 0.1 s
        ticker(start=0, end=0.9, major_count=7)
        ticks = ticker.major_ticks()
        
        model = (0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9)
        assert_array_almost_equal(ticks, model)
    
    
    def test_beautify(self):
        """Tests whether beautify function works correctly."""
        
        ticker = pero.TimeTicker()
        
        # test hours
        beautified = ticker.beautify(2.1*3600, 5.7*3600)
        self.assertEqual(beautified, (2*3600, 6*3600))
        
        beautified = ticker.beautify(5.7*3600, 2.1*3600)
        self.assertEqual(beautified, (6*3600, 2*3600))
        
        # test minutes
        beautified = ticker.beautify(7*60, 48*60)
        self.assertEqual(beautified, (5*60, 50*60))
        
        beautified = ticker.beautify(48*60, 7*60)
        self.assertEqual(beautified, (50*60, 5*60))


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
