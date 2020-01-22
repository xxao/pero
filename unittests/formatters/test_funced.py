#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for custom function formatter."""
    
    
    def test_formatter(self):
        """Tests whether formatter works as standalone tool."""
        
        formatter = pero.FuncFormatter(func=lambda d: "{:0.2f} u".format(d))
        
        self.assertEqual(formatter.format(0), "0.00 u")
        self.assertEqual(formatter.format(1.5), "1.50 u")
        self.assertEqual(formatter.format(1e6), "1000000.00 u")


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
