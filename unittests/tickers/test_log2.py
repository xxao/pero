#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for logarithmic ticker with base 2."""
    
    
    def test_major_ticks(self):
        """Tests whether major ticks are generated works correctly."""
        
        # init ticker
        ticker = pero.LogTicker(base=2, major_count=7)
        
        # test above one
        ticker(start=1.1, end=0.9e3)
        ticks = ticker.major_ticks()
        self.assertEqual(ticks, (2, 4, 8, 16, 32, 64, 128, 256, 512))
        
        # test one
        ticker(start=1, end=0.9e3)
        ticks = ticker.major_ticks()
        self.assertEqual(ticks, (1, 2, 4, 8, 16, 32, 64, 128, 256, 512))
        
        # test below one
        ticker(start=0.1, end=0.9)
        ticks = ticker.major_ticks()
        self.assertEqual(ticks, (0.125, 0.25, 0.5))
        
        # test cross one
        ticker(start=0.1, end=9)
        ticks = ticker.major_ticks()
        self.assertEqual(ticks, (0.125, 0.25, 0.5, 1, 2, 4, 8))
        
        # test condensed
        ticker(start=1, end=1e7)
        ticks = ticker.major_ticks()
        self.assertEqual(ticks, (1, 16, 256, 4096, 65536, 1048576))
        
        # test flipped
        ticker(start=9, end=0.1)
        ticks = ticker.major_ticks()
        self.assertEqual(ticks, (8, 4, 2, 1, 0.5, 0.25, 0.125))
    
    
    def test_minor_ticks(self):
        """Tests whether minor ticks are generated correctly."""
        
        # init ticker
        ticker = pero.LogTicker(base=2, major_count=7, minor_count=4)
        
        # test above one
        ticker(start=1.1, end=0.9e3)
        ticks = ticker.minor_ticks()
        self.assertEqual(ticks, (2, 4, 8, 16, 32, 64, 128, 256, 512))
        
        # test one
        ticker(start=1, end=0.9e3)
        ticks = ticker.minor_ticks()
        self.assertEqual(ticks, (1, 2, 4, 8, 16, 32, 64, 128, 256, 512))
        
        # test below one
        ticker(start=0.1, end=0.9)
        ticks = ticker.minor_ticks()
        self.assertEqual(ticks, (0.125, 0.25, 0.5))
        
        # test cross one
        ticker(start=0.1, end=9)
        ticks = ticker.minor_ticks()
        self.assertEqual(ticks, (0.125, 0.25, 0.5, 1, 2, 4, 8))
        
        # test condensed
        ticker(start=1, end=1e4)
        ticks = ticker.minor_ticks()
        self.assertEqual(ticks, (1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192))
        
        # test flipped
        ticker(start=9, end=0.1)
        ticks = ticker.minor_ticks()
        self.assertEqual(ticks, (8, 4, 2, 1, 0.5, 0.25, 0.125))
    
    
    def test_beautify(self):
        """Tests whether beautify function works correctly."""
        
        # init ticker
        ticker = pero.LogTicker(base=2, major_count=7)
        
        # test above one
        beautified = ticker.beautify(1.1, 0.9e3)
        self.assertEqual(beautified, (1, 1024))
        
        # test one
        beautified = ticker.beautify(1, 0.9e3)
        self.assertEqual(beautified, (1, 1024))
        
        # test below one
        beautified = ticker.beautify(0.1, 0.9)
        self.assertEqual(beautified, (0.0625, 1))
        
        # test cross one
        beautified = ticker.beautify(0.9, 1.1e3)
        self.assertEqual(beautified, (0.5, 2048))
        
        # test flipped
        beautified = ticker.beautify(0.9e3, 0.9)
        self.assertEqual(beautified, (1024, 0.5))


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
