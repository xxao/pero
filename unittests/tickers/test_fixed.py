#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for fixed values ticker."""
    
    
    def test_major_ticks(self):
        """Tests whether major ticks are calculated correctly."""
        
        ticker = pero.FixTicker(major_values=(2, 4, 8, 16))
        
        # test within range
        ticker(start=5, end=10)
        ticks = ticker.major_ticks()
        self.assertEqual(ticks, (8,))
        
        # test outside range
        ticker(start=100, end=1000)
        ticks = ticker.major_ticks()
        self.assertEqual(ticks, ())
        
        # test cross range
        ticker(start=5, end=1000)
        ticks = ticker.major_ticks()
        self.assertEqual(ticks, (8, 16))
        
        # test flipped
        ticker(start=1000, end=5)
        ticks = ticker.major_ticks()
        self.assertEqual(ticks, (8, 16))
    
    
    def test_minor_ticks(self):
        """Tests whether minor ticks are calculated correctly."""
        
        ticker = pero.FixTicker(minor_values=(2, 3, 4, 6, 8, 12, 16))
        
        # test within range
        ticker(start=5, end=10)
        ticks = ticker.minor_ticks()
        self.assertEqual(ticks, (6, 8))
        
        # test outside range
        ticker(start=100, end=1000)
        ticks = ticker.minor_ticks()
        self.assertEqual(ticks, ())
        
        # test cross range
        ticker(start=5, end=1000)
        ticks = ticker.minor_ticks()
        self.assertEqual(ticks, (6, 8, 12, 16))
        
        # test flipped
        ticker(start=1000, end=5)
        ticks = ticker.minor_ticks()
        self.assertEqual(ticks, (6, 8, 12, 16))


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
