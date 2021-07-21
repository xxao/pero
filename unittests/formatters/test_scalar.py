#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for scalar formatter."""
    
    
    def test_auto_range(self):
        """Tests whether domain together with precision are used correctly."""
        
        formatter = pero.ScalarFormatter(
            domain = 7e6,
            precision = 100,
            sci_notation = False)
        
        self.assertEqual(formatter.format(0), "0")
        self.assertEqual(formatter.format(0.123456), "0")
        self.assertEqual(formatter.format(1.23456), "1")
        self.assertEqual(formatter.format(123.456), "123")
        self.assertEqual(formatter.format(1234.56), "1235")
        
        formatter = pero.ScalarFormatter(
            domain = 7e3,
            precision = 0.5,
            sci_notation = False)
        
        self.assertEqual(formatter.format(0), "0.0")
        self.assertEqual(formatter.format(0.123456), "0.1")
        self.assertEqual(formatter.format(1.23456), "1.2")
        self.assertEqual(formatter.format(123.456), "123.5")
        self.assertEqual(formatter.format(1234.56), "1234.6")
        
        formatter = pero.ScalarFormatter(
            domain = 7e-3,
            precision = 0.0005,
            sci_notation = False)
        
        self.assertEqual(formatter.format(0), "0.0000")
        self.assertEqual(formatter.format(0.123456), "0.1235")
        self.assertEqual(formatter.format(1.23456), "1.2346")
        self.assertEqual(formatter.format(123.456), "123.4560")
        self.assertEqual(formatter.format(1234.56), "1234.5600")
    
    
    def test_sci_notation(self):
        """Tests whether scientific notation works correctly."""
        
        formatter = pero.ScalarFormatter(
            domain = 7e6,
            precision = 100,
            sci_notation = True,
            sci_threshold = 3)
        
        self.assertEqual(formatter.format(0), "0e+00")
        self.assertEqual(formatter.format(0.123456), "1e-01")
        self.assertEqual(formatter.format(1.23456), "1e+00")
        self.assertEqual(formatter.format(123.456), "1e+02")
        self.assertEqual(formatter.format(1234.56), "1.2e+03")
        
        formatter = pero.ScalarFormatter(
            domain = 7e3,
            precision = 0.1,
            sci_notation = True,
            sci_threshold = 3)
        
        self.assertEqual(formatter.format(0), "0e+00")
        self.assertEqual(formatter.format(0.123456), "1e-01")
        self.assertEqual(formatter.format(1.23456), "1.2e+00")
        self.assertEqual(formatter.format(123.456), "1.235e+02")
        self.assertEqual(formatter.format(1234.56), "1.2346e+03")
        
        formatter = pero.ScalarFormatter(
            domain = 7e-3,
            precision = 0.001,
            sci_notation = True,
            sci_threshold = 3)
        
        self.assertEqual(formatter.format(0), "0e+00")
        self.assertEqual(formatter.format(0.123456), "1.23e-01")
        self.assertEqual(formatter.format(1.23456), "1.235e+00")
        self.assertEqual(formatter.format(123.456), "1.23456e+02")
        self.assertEqual(formatter.format(1234.56), "1.234560e+03")
    
    
    def test_suffix(self):
        """Tests whether suffix works correctly."""
        
        formatter = pero.ScalarFormatter(
            domain = 7e6,
            precision = 100,
            sci_notation = True,
            sci_threshold = 3,
            hide_suffix = True,
            suffix_template = "e{:.0f}")
        
        self.assertEqual(formatter.suffix(), "e6")
        
        self.assertEqual(formatter.format(0), "0.0000")
        self.assertEqual(formatter.format(0.123456), "0.0000")
        self.assertEqual(formatter.format(1.23456), "0.0000")
        self.assertEqual(formatter.format(123.456), "0.0001")
        self.assertEqual(formatter.format(1234.56), "0.0012")
        
        formatter = pero.ScalarFormatter(
            domain = 7e3,
            precision = 0.1,
            sci_notation = True,
            sci_threshold = 3,
            hide_suffix = True,
            suffix_template = "e{:.0f}")
        
        self.assertEqual(formatter.suffix(), "e3")
        
        self.assertEqual(formatter.format(0), "0.0000")
        self.assertEqual(formatter.format(0.123456), "0.0001")
        self.assertEqual(formatter.format(1.23456), "0.0012")
        self.assertEqual(formatter.format(123.456), "0.1235")
        self.assertEqual(formatter.format(1234.56), "1.2346")
        
        formatter = pero.ScalarFormatter(
            domain = 7e-3,
            precision = 0.001,
            sci_notation = True,
            sci_threshold = 3,
            hide_suffix = True,
            suffix_template = "e{:.0f}")
        
        self.assertEqual(formatter.suffix(), "e-3")
        
        self.assertEqual(formatter.format(0), "0")
        self.assertEqual(formatter.format(0.123456), "123")
        self.assertEqual(formatter.format(1.23456), "1235")
        self.assertEqual(formatter.format(123.456), "123456")
        self.assertEqual(formatter.format(1234.56), "1234560")


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
