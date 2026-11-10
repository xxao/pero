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
    
    
    def test_calc_power(self):
        """Tests whether power is calculated correctly."""
        
        self.assertEqual(pero.formatters.calc_power(1000), 3)
        self.assertEqual(pero.formatters.calc_power(999), 2)
        self.assertEqual(pero.formatters.calc_power(0.001), -3)
        self.assertEqual(pero.formatters.calc_power(1024, 2), 10)
        self.assertEqual(pero.formatters.calc_power(1023, 2), 9)
        self.assertEqual(pero.formatters.calc_power(2.5**6, 2.5), 6)
    
    
    def test_calc_digits(self):
        """Tests whether decimal places are calculated correctly."""
        
        self.assertEqual(pero.formatters.calc_digits(100), 0)
        self.assertEqual(pero.formatters.calc_digits(1), 0)
        self.assertEqual(pero.formatters.calc_digits(0.05), 2)
        self.assertEqual(pero.formatters.calc_digits(-0.05), 2)
        self.assertEqual(pero.formatters.calc_digits(None), 0)
        self.assertEqual(pero.formatters.calc_digits(1, 1000), 3)
        self.assertEqual(pero.formatters.calc_digits(100, 10, 3), 1)
        self.assertEqual(pero.formatters.calc_digits(None, 10, -3), 0)
        self.assertEqual(pero.formatters.calc_digits(0.01, 2, 9), 5)
        self.assertEqual(pero.formatters.calc_digits(1, 2, 1100), 332)
    
    
    def test_strip_negative_zero(self):
        """Tests whether minus sign is removed from zero only."""
        
        self.assertEqual(pero.formatters.strip_negative_zero("-0.00", "0.00"), "0.00")
        self.assertEqual(pero.formatters.strip_negative_zero("-0.00 k", "0.00 k"), "0.00 k")
        self.assertEqual(pero.formatters.strip_negative_zero("-0.01", "0.00"), "-0.01")
        self.assertEqual(pero.formatters.strip_negative_zero("0.00", "0.00"), "0.00")
        self.assertEqual(pero.formatters.strip_negative_zero("-inf", "0"), "-inf")


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
