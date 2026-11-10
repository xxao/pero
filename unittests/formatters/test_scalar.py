#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import math
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
            sci_notation = False,
            trim_zeros = False)
        
        self.assertEqual(formatter.format(0), "0")
        self.assertEqual(formatter.format(0.123456), "0.1")
        self.assertEqual(formatter.format(1.23456), "1.2")
        self.assertEqual(formatter.format(123.456), "123.5")
        self.assertEqual(formatter.format(1234.56), "1234.6")
        
        formatter = pero.ScalarFormatter(
            domain = 7e-3,
            precision = 0.0005,
            sci_notation = False,
            trim_zeros = False)
        
        self.assertEqual(formatter.format(0), "0")
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
        
        self.assertEqual(formatter.format(0), "0")
        self.assertEqual(formatter.format(0.123456), "1e-01")
        self.assertEqual(formatter.format(1.23456), "1e+00")
        self.assertEqual(formatter.format(123.456), "1e+02")
        self.assertEqual(formatter.format(1234.56), "1.2e+03")
        
        formatter = pero.ScalarFormatter(
            domain = 7e3,
            precision = 0.1,
            sci_notation = True,
            sci_threshold = 3)
        
        self.assertEqual(formatter.format(0), "0")
        self.assertEqual(formatter.format(0.123456), "1e-01")
        self.assertEqual(formatter.format(1.23456), "1.2e+00")
        self.assertEqual(formatter.format(123.456), "1.235e+02")
        self.assertEqual(formatter.format(1234.56), "1.2346e+03")
        
        formatter = pero.ScalarFormatter(
            domain = 7e-3,
            precision = 0.001,
            sci_notation = True,
            sci_threshold = 3,
            trim_zeros = False)
        
        self.assertEqual(formatter.format(0), "0")
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
            suffix_template = "e{:.0f}",
            trim_zeros = False)
        
        self.assertEqual(formatter.suffix(), "e6")
        
        self.assertEqual(formatter.format(0), "0")
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
            suffix_template = "e{:.0f}",
            trim_zeros = False)
        
        self.assertEqual(formatter.suffix(), "e3")
        
        self.assertEqual(formatter.format(0), "0")
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
    
    
    def test_trim_zeros(self):
        """Tests whether zero trimmin works correctly."""
        
        formatter = pero.ScalarFormatter(
            domain = 1e40,
            precision = 1,
            trim_zeros = True)
        
        self.assertEqual(formatter.format(1e24), "1e+24")
        self.assertEqual(formatter.format(1e30), "1e+30")
        self.assertEqual(formatter.format(1e40), "1e+40")
        self.assertEqual(formatter.format(1.25e40), "1.25e+40")
        self.assertEqual(formatter.format(-1e40), "-1e+40")
        
        formatter.precision = 100
        self.assertEqual(formatter.format(12345.6), "1.23e+04")
    
    
    def test_base_two(self):
        """Tests whether binary base works correctly."""
        
        formatter = pero.ScalarFormatter(
            base = 2,
            domain = 1024,
            precision = 0.001)
        
        self.assertEqual(formatter.format(0), "0")
        self.assertEqual(formatter.format(-0.0), "0")
        self.assertEqual(formatter.format(0.125), "2^-3")
        self.assertEqual(formatter.format(3), "1.5×2^1")
        self.assertEqual(formatter.format(512), "2^9")
        self.assertEqual(formatter.format(768), "1.5×2^9")
        self.assertEqual(formatter.format(-512), "-2^9")
        self.assertEqual(formatter.format(-768), "-1.5×2^9")
        
        formatter.precision = 100
        self.assertEqual(formatter.format(768), "1.5×2^9")
        self.assertEqual(formatter.format(1023), "2^10")
        self.assertEqual(formatter.format(-1023), "-2^10")
        
        formatter(domain=2.**100, precision=1)
        self.assertEqual(formatter.format(2.**100), "2^100")
    
    
    def test_other_bases(self):
        """Tests whether non-binary bases work correctly."""
        
        formatter = pero.ScalarFormatter(
            base = 3,
            domain = 243,
            precision = 0.001)
        
        self.assertEqual(formatter.format(243), "3^5")
        self.assertEqual(formatter.format(1 / 243), "3^-5")
        
        formatter(base=2.5, domain=2.5**6)
        self.assertEqual(formatter.format(2.5**6), "2.5^6")
        self.assertEqual(formatter.format(9.375), "1.5×2.5^2")
        
        formatter(base=2.123456789, sci_threshold=0)
        self.assertEqual(formatter.format(2.123456789**2), "2.123456789^2")
    
    
    def test_base_threshold(self):
        """Tests whether threshold is used as a power of base."""
        
        formatter = pero.ScalarFormatter(
            base = 2,
            domain = 31,
            precision = 0.001)
        
        self.assertEqual(formatter.format(16), "16")
        
        formatter.domain = 32
        self.assertEqual(formatter.format(16), "2^4")
        
        formatter.domain = 2.**-5
        self.assertEqual(formatter.format(2.**-5), "2^-5")
        
        formatter.domain = 2.**-4
        self.assertEqual(formatter.format(2.**-4), "0.062")
    
    
    def test_base_precision(self):
        """Tests whether precision is used independently of base."""
        
        formatter = pero.ScalarFormatter(
            base = 2,
            domain = 512,
            precision = 0.001,
            sci_notation = False)
        
        self.assertEqual(formatter.format(0.125), "0.125")
        self.assertEqual(formatter.format(-0.0001), "0")
        
        formatter(sci_notation=True, precision=0.01, trim_zeros=False)
        self.assertEqual(formatter.format(3), "1.500×2^1")
        self.assertEqual(formatter.format(512), "1.00000×2^9")
    
    
    def test_base_suffix(self):
        """Tests whether suffix works correctly with base."""
        
        formatter = pero.ScalarFormatter(
            base = 2,
            domain = 512,
            precision = 1,
            hide_suffix = True,
            trim_zeros = False)
        
        self.assertEqual(formatter.suffix(), " (×2^9)")
        
        self.assertEqual(formatter.format(512), "1.000")
        self.assertEqual(formatter.format(-512), "-1.000")
        self.assertEqual(formatter.format(-0.125), "0.000")
        
        formatter.trim_zeros = True
        self.assertEqual(formatter.format(512), "1")
        self.assertEqual(formatter.format(768), "1.5")
        
        formatter.suffix_template = "power {:.0f}"
        self.assertEqual(formatter.suffix(), "power 9")
        
        formatter.suffix_template = " [{base}^{power}]"
        self.assertEqual(formatter.suffix(), " [2^9]")
        
        formatter.suffix_template = ""
        self.assertEqual(formatter.suffix(), "")
        
        formatter.suffix_template = None
        self.assertEqual(formatter.suffix(), "")
        
        formatter(suffix_template=pero.UNDEF, base=10, domain=1e6)
        self.assertEqual(formatter.suffix(), " (e6)")
    
    
    def test_base_changes(self):
        """Tests whether base changes are applied correctly."""
        
        formatter = pero.ScalarFormatter(
            domain = 512,
            precision = 1)
        
        self.assertEqual(formatter.format(512), "512")
        
        formatter.base = 2
        self.assertEqual(formatter.format(512), "2^9")
        
        formatter.hide_suffix = True
        self.assertEqual(formatter.format(512), "1")
        self.assertEqual(formatter.suffix(), " (×2^9)")
        
        formatter.base = 10
        self.assertEqual(formatter.format(512), "512")
        self.assertEqual(formatter.suffix(), "")


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
