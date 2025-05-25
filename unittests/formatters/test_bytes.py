#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for bytes formatter."""
    
    
    def test_standalone(self):
        """Tests whether formatter works as standalone tool."""
        
        formatter = pero.BytesFormatter()
        
        self.assertEqual(formatter.format(234.5678e6), "224 MB")
        self.assertEqual(formatter.format(234.5678e3), "229 kB")
        self.assertEqual(formatter.format(234.5678), "235 B")
        self.assertEqual(formatter.format(234.5678e-3), "0 B")
    
    
    def test_places(self):
        """Tests whether places works correctly."""
        
        formatter = pero.BytesFormatter(places=0)
        
        self.assertEqual(formatter.format(234.5678e6), "224 MB")
        self.assertEqual(formatter.format(234.5678e3), "229 kB")
        self.assertEqual(formatter.format(234.5678), "235 B")
        self.assertEqual(formatter.format(234.5678e-3), "0 B")
        self.assertEqual(formatter.format(234.5678e-6), "0 B")
        
        formatter = pero.BytesFormatter(places=2)
        
        self.assertEqual(formatter.format(234.5678e6), "223.70 MB")
        self.assertEqual(formatter.format(234.5678e3), "229.07 kB")
        self.assertEqual(formatter.format(234.5678), "234.57 B")
        self.assertEqual(formatter.format(234.5678e-3), "0.23 B")
        self.assertEqual(formatter.format(234.5678e-6), "0.00 B")
    
    
    def test_precision(self):
        """Tests whether precision works correctly."""
        
        formatter = pero.BytesFormatter(precision=200)
        
        self.assertEqual(formatter.format(234.5678e6), "223.7013 MB")
        self.assertEqual(formatter.format(234.5678e3), "229.1 kB")
        self.assertEqual(formatter.format(234.5678), "235 B")
        self.assertEqual(formatter.format(234.5678e-3), "0 B")
        self.assertEqual(formatter.format(234.5678e-6), "0 B")
        
        formatter = pero.BytesFormatter(precision=0.2)
        
        self.assertEqual(formatter.format(234.5678e6), "223.7012863 MB")
        self.assertEqual(formatter.format(234.5678e3), "229.0701 kB")
        self.assertEqual(formatter.format(234.5678), "234.6 B")
        self.assertEqual(formatter.format(234.5678e-3), "0.2 B")
        self.assertEqual(formatter.format(234.5678e-6), "0.0 B")
    
    
    def test_domain(self):
        """Tests whether domain works correctly."""
        
        formatter = pero.BytesFormatter(domain=1e4)
        
        self.assertEqual(formatter.format(234.5678e6), "229070 kB")
        self.assertEqual(formatter.format(234.5678e3), "229 kB")
        self.assertEqual(formatter.format(234.5678), "0 kB")
        self.assertEqual(formatter.format(234.5678e-3), "0 kB")
        self.assertEqual(formatter.format(234.5678e-6), "0 kB")
        
        formatter = pero.BytesFormatter(domain=1e2)
        
        self.assertEqual(formatter.format(234.5678e6), "234567800 B")
        self.assertEqual(formatter.format(234.5678e3), "234568 B")
        self.assertEqual(formatter.format(234.5678), "235 B")
        self.assertEqual(formatter.format(234.5678e-3), "0 B")
        self.assertEqual(formatter.format(234.5678e-6), "0 B")
    
    
    def test_digits(self):
        """Tests whether digits works correctly."""
        
        # check domain and precision
        formatter = pero.BytesFormatter(domain=1e4, precision=200)
        
        self.assertEqual(formatter.format(234.5678e6), "229070.1 kB")
        self.assertEqual(formatter.format(234.5678e3), "229.1 kB")
        self.assertEqual(formatter.format(234.5678), "0.2 kB")
        self.assertEqual(formatter.format(234.5678e-3), "0.0 kB")
        self.assertEqual(formatter.format(234.5678e-6), "0.0 kB")
        
        # check domain, precision and places
        formatter = pero.BytesFormatter(domain=1e4, precision=200, places=2)
        
        self.assertEqual(formatter.format(234.5678e6), "229070.12 kB")
        self.assertEqual(formatter.format(234.5678e3), "229.07 kB")
        self.assertEqual(formatter.format(234.5678), "0.23 kB")
        self.assertEqual(formatter.format(234.5678e-3), "0.00 kB")
        self.assertEqual(formatter.format(234.5678e-6), "0.00 kB")
    
    
    def test_suffix(self):
        """Tests whether suffix works correctly."""
        
        # standalone formatter
        formatter = pero.BytesFormatter(hide_suffix=True)
        self.assertEqual(formatter.suffix(), "")
        
        self.assertEqual(formatter.format(234.5678e6), "224")
        self.assertEqual(formatter.suffix(), " (MB)")
        
        self.assertEqual(formatter.format(234.5678e3), "229")
        self.assertEqual(formatter.suffix(), " (kB)")
        
        self.assertEqual(formatter.format(234.5678), "235")
        self.assertEqual(formatter.suffix(), " (B)")
        
        # formatter with domain
        formatter = pero.BytesFormatter(hide_suffix=True, domain=1e4)
        self.assertEqual(formatter.suffix(), " (kB)")
        
        self.assertEqual(formatter.format(234.5678e6), "229070")
        self.assertEqual(formatter.suffix(), " (kB)")
        
        self.assertEqual(formatter.format(234.5678e3), "229")
        self.assertEqual(formatter.suffix(), " (kB)")
        
        self.assertEqual(formatter.format(234.5678), "0")
        self.assertEqual(formatter.suffix(), " (kB)")
    
    
    def test_convert(self):
        """Tests whether convert works correctly."""
        
        formatter = pero.BytesFormatter(domain=1e4)
        
        self.assertEqual(formatter.convert(234.5678e6), 229070.1171875)
        self.assertEqual(formatter.convert(234.5678e4), 2290.701171875)
        self.assertEqual(formatter.convert(234.5678), 0.2290701171875)
        self.assertEqual(formatter.convert(234.5678e-4), 2.290701171875e-05)
        self.assertEqual(formatter.convert(234.5678e-6), 2.290701171875e-07)
    
    
    def test_invert(self):
        """Tests whether invert works correctly."""
        
        formatter = pero.BytesFormatter(domain=1e4)
        
        self.assertEqual(formatter.invert(229070.1171875), 234.5678e6)
        self.assertEqual(formatter.invert(2290.701171875), 234.5678e4)
        self.assertEqual(formatter.invert(0.2290701171875), 234.5678)
        self.assertEqual(formatter.invert(2.290701171875e-05), 234.5678e-4)
        self.assertEqual(formatter.invert(2.290701171875e-07), 234.5678e-6)


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
