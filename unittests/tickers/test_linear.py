#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for linear ticker."""
    
    
    def test_major_ticks(self):
        """Tests whether major ticks are calculated correctly."""
        
        ticker = pero.LinTicker(major_splits=(5,3,2))
        
        # test ascending
        ticker(start=0, end=10, major_count=3)
        ticks = ticker.major_ticks()
        
        model = (0, 3, 6, 9)
        self.assertEqual(ticks, model)
        
        ticker(start=0, end=.1, major_count=5)
        ticks = ticker.major_ticks()
        
        model = (0, .02, .04, .06, .08, .1)
        self.assertEqual(ticks, model)
        
        # test descending
        ticker(start=10, end=0, major_count=3)
        ticks = ticker.major_ticks()
        
        model = (9, 6, 3, 0)
        self.assertEqual(ticks, model)
    
    
    def test_minor_ticks(self):
        """Tests whether minor ticks are calculated correctly."""
        
        ticker = pero.LinTicker(major_splits=(5,3,2))
        
        # test ascending
        ticker(start=0, end=10, major_count=3, minor_count=5)
        ticks = ticker.minor_ticks()
        
        model = (0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10)
        self.assertEqual(ticks, model)
        
        # test descending
        ticker(start=10, end=0, major_count=3, minor_count=5)
        ticks = ticker.minor_ticks()
        
        model = (10.0, 9.5, 9.0, 8.5, 8.0, 7.5, 7.0, 6.5, 6.0, 5.5, 5.0, 4.5, 4.0, 3.5, 3.0, 2.5, 2.0, 1.5, 1.0, 0.5, 0.0)
        self.assertEqual(ticks, model)
    
    
    def test_format(self):
        """Tests whether labels are formatted correctly."""
        
        # test small values
        ticker = pero.LinTicker(start=0, end=10)
        
        label = ticker.format(0.2)
        self.assertEqual(label, "0")
        
        label = ticker.format(2.7)
        self.assertEqual(label, "3")
        
        # test custom string format
        formatter = pero.StrFormatter(template="{:0.1f} u")
        ticker = pero.LinTicker(start=0, end=10, formatter=formatter)
        
        label = ticker.format(0.2)
        self.assertEqual(label, "0.2 u")
        
        # test custom function format
        formatter = pero.FuncFormatter(func=lambda x:"{:.3f} u".format(x))
        ticker = pero.LinTicker(start=0, end=10, formatter=formatter)
        
        label = ticker.format(0.2)
        self.assertEqual(label, "0.200 u")
        
        # test scientific notation
        ticker = pero.LinTicker(start=0, end=1e7)
        ticker.formatter.sci_notation = True
        
        label = ticker.format(2700000)
        self.assertEqual(label, "3e+06")
        
        # test suffix
        ticker = pero.LinTicker(start=0, end=1e7)
        ticker.formatter.sci_notation = True
        ticker.formatter.hide_suffix = True
        ticker.formatter.suffix_template = "10^{:0.0f}"
        
        suffix = ticker.suffix()
        self.assertEqual(suffix, "10^7")
    
    
    def test_beautify(self):
        """Tests whether beautify function works correctly."""
        
        ticker = pero.LinTicker()
        
        # test ascending
        beautified = ticker.beautify(0.201, 0.99)
        self.assertEqual(beautified, (0.2, 1))
        
        # test descending
        beautified = ticker.beautify(0.99, 0.201)
        self.assertEqual(beautified, (1, 0.2))


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
