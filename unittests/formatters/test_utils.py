#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for ticker helpers."""
    
    
    def test_split_time(self):
        """Tests whether time splits are calculated correctly."""
        
        parts = pero.formatters.split_time(5555.1234567890123)
        model = {"d": 0, "h": 1, "m": 32, "s": 35, "ms": 123, "us": 456, "ns": 789}
        self.assertEqual(parts, model)
        
        parts = pero.formatters.split_time(55)
        model = {"d": 0, "h": 0, "m": 0, "s": 55, "ms": 0, "us": 0, "ns": 0}
        self.assertEqual(parts, model)


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
