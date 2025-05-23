#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for ticker helpers."""
    
    
    def test_split_eng(self):
        """Tests whether engineering splits are calculated correctly."""
        
        splits = pero.SPLITS_ENG
        
        parts = pero.formatters.split_value(12345, splits)
        model = {k: 0 for k in splits}
        model.update({"k": 12, "": 345})
        self.assertEqual(parts, model)
    
    
    def test_split_time(self):
        """Tests whether time splits are calculated correctly."""
        
        splits = pero.SPLITS_TIME
        
        parts = pero.formatters.split_value(12345.6789, splits)
        model = {k: 0 for k in splits}
        model.update({"h": 3, "m": 25, "s": 45, "ms": 678, "us": 900})
        self.assertEqual(parts, model)
    
    
    def test_split_bytes(self):
        """Tests whether bytes splits are calculated correctly."""
        
        splits = pero.SPLITS_BYTES
        
        parts = pero.formatters.split_value(1234567.89, splits)
        model = {k: 0 for k in splits}
        model.update({"M": 1, "k": 181, "": 647})
        self.assertEqual(parts, model)


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
