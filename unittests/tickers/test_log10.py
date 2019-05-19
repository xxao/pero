#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for logarithmic ticker with base 10."""
    
    
    def test_major_ticks(self):
        """Tests whether major ticks are generated works correctly."""
        
        # init ticker
        ticker = pero.LogTicker()
        
        # test above one
        ticker(start=1.1, end=0.9e3)
        ticks = ticker.major_ticks()
        self.assertEqual(ticks, (1e1, 1e2))
        
        # test one
        ticker(start=1, end=1.1e3)
        ticks = ticker.major_ticks()
        self.assertEqual(ticks, (1, 1e1, 1e2, 1e3))
        
        # test below one
        ticker(start=0.9e-5, end=1.1e-2)
        ticks = ticker.major_ticks()
        self.assertEqual(ticks, (1e-5, 1e-4, 1e-3, 1e-2))
        
        # test cross one
        ticker(start=0.09, end=1.1e3)
        ticks = ticker.major_ticks()
        self.assertEqual(ticks, (.1, 1, 1e1, 1e2, 1e3))
        
        # test condensed
        ticker(start=1, end=1e10)
        ticks = ticker.major_ticks()
        self.assertEqual(ticks, (1.0, 1e2, 1e4, 1e6, 1e8, 1e10))
        
        # test flipped
        ticker(start=1.1e3, end=0.9)
        ticks = ticker.major_ticks()
        self.assertEqual(ticks, (1e3, 1e2, 1e1, 1))
        
        # test small
        ticker(start=1.1, end=1.2)
        ticks = ticker.major_ticks()
        ticks = tuple(map(lambda x:round(x,2), ticks))
        self.assertEqual(ticks, (1.1, 1.12, 1.14, 1.16, 1.18))
    
    
    def test_minor_ticks(self):
        """Tests whether minor ticks are generated correctly."""
        
        # init ticker
        ticker = pero.LogTicker()
        
        # test step one
        ticker(start=1.1, end=0.9e2)
        ticks = ticker.minor_ticks()
        self.assertEqual(ticks, (2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90))
        
        # test flipped
        ticker(start=0.9e2, end=1.1)
        ticks = ticker.minor_ticks()
        self.assertEqual(ticks, (90, 80, 70, 60, 50, 40, 30, 20, 10, 9, 8, 7, 6, 5, 4, 3, 2))
        
        # test step grater than one
        ticker(start=1, end=1e14)
        ticks = ticker.minor_ticks()
        self.assertEqual(ticks, (1.0, 10, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9, 1e10, 1e11, 1e12, 1e13, 1e14))
    
    
    def test_beautify(self):
        """Tests whether beautify function works correctly."""
        
        # init ticker
        ticker = pero.LogTicker()
        
        # test above one
        beautified = ticker.beautify(1.1, 0.9e3)
        self.assertEqual(beautified, (1, 1000))
        
        # test one
        beautified = ticker.beautify(1, 0.9e3)
        self.assertEqual(beautified, (1, 1000))
        
        # test below one
        beautified = ticker.beautify(0.9e-5, 1.1e-2)
        self.assertEqual(beautified, (1e-6, 1e-1))
        
        # test cross one
        beautified = ticker.beautify(0.9, 1.1e3)
        self.assertEqual(beautified, (0.1, 10000))
        
        # test flipped
        beautified = ticker.beautify(0.9e3, 0.9)
        self.assertEqual(beautified, (1000, 0.1))


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
