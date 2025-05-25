#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for engineering formatter."""
    
    
    def test_standalone(self):
        """Tests whether formatter works as standalone tool."""
        
        formatter = pero.EngFormatter()
        
        self.assertEqual(formatter.format(234.5678e6), "235 M")
        self.assertEqual(formatter.format(234.5678e3), "235 k")
        self.assertEqual(formatter.format(234.5678), "235")
        self.assertEqual(formatter.format(234.5678e-3), "235 m")
        self.assertEqual(formatter.format(234.5678e-6), "235 u")
    
    
    def test_units(self):
        """Tests whether units are added correctly."""
        
        formatter = pero.EngFormatter(units="Hz")
        
        self.assertEqual(formatter.format(234.5678e6), "235 MHz")
        self.assertEqual(formatter.format(234.5678e3), "235 kHz")
        self.assertEqual(formatter.format(234.5678), "235 Hz")
        self.assertEqual(formatter.format(234.5678e-3), "235 mHz")
        self.assertEqual(formatter.format(234.5678e-6), "235 uHz")
    
    
    def test_places(self):
        """Tests whether places works correctly."""
        
        formatter = pero.EngFormatter(places=0)
        
        self.assertEqual(formatter.format(234.5678e6), "235 M")
        self.assertEqual(formatter.format(234.5678e3), "235 k")
        self.assertEqual(formatter.format(234.5678), "235")
        self.assertEqual(formatter.format(234.5678e-3), "235 m")
        self.assertEqual(formatter.format(234.5678e-6), "235 u")
        
        formatter = pero.EngFormatter(places=2)
        
        self.assertEqual(formatter.format(234.5678e6), "234.57 M")
        self.assertEqual(formatter.format(234.5678e3), "234.57 k")
        self.assertEqual(formatter.format(234.5678), "234.57")
        self.assertEqual(formatter.format(234.5678e-3), "234.57 m")
        self.assertEqual(formatter.format(234.5678e-6), "234.57 u")
    
    
    def test_precision(self):
        """Tests whether precision works correctly."""
        
        formatter = pero.EngFormatter(precision=100)
        
        self.assertEqual(formatter.format(234.5678e6), "234.5678 M")
        self.assertEqual(formatter.format(234.5678e3), "234.6 k")
        self.assertEqual(formatter.format(234.5678), "235")
        self.assertEqual(formatter.format(234.5678e-3), "235 m")
        self.assertEqual(formatter.format(234.5678e-6), "235 u")
        
        formatter = pero.EngFormatter(precision=0.1)
        
        self.assertEqual(formatter.format(234.5678e6), "234.5678000 M")
        self.assertEqual(formatter.format(234.5678e3), "234.5678 k")
        self.assertEqual(formatter.format(234.5678), "234.6")
        self.assertEqual(formatter.format(234.5678e-3), "235 m")
        self.assertEqual(formatter.format(234.5678e-6), "235 u")
    
    
    def test_domain(self):
        """Tests whether domain works correctly."""
        
        formatter = pero.EngFormatter(domain=1e4)
        
        self.assertEqual(formatter.format(234.5678e6), "234568 k")
        self.assertEqual(formatter.format(234.5678e3), "235 k")
        self.assertEqual(formatter.format(234.5678), "0 k")
        self.assertEqual(formatter.format(234.5678e-3), "0 k")
        self.assertEqual(formatter.format(234.5678e-6), "0 k")
        
        formatter = pero.EngFormatter(domain=1e2)
        
        self.assertEqual(formatter.format(234.5678e6), "234567800")
        self.assertEqual(formatter.format(234.5678e3), "234568")
        self.assertEqual(formatter.format(234.5678), "235")
        self.assertEqual(formatter.format(234.5678e-3), "0")
        self.assertEqual(formatter.format(234.5678e-6), "0")
    
    
    def test_digits(self):
        """Tests whether digits works correctly."""
        
        # check domain and precision
        formatter = pero.EngFormatter(domain=1e4, precision=100)
        
        self.assertEqual(formatter.format(234.5678e6), "234567.8 k")
        self.assertEqual(formatter.format(234.5678e3), "234.6 k")
        self.assertEqual(formatter.format(234.5678), "0.2 k")
        self.assertEqual(formatter.format(234.5678e-3), "0.0 k")
        self.assertEqual(formatter.format(234.5678e-6), "0.0 k")
        
        # check domain, precision and places
        formatter = pero.EngFormatter(domain=1e4, precision=100, places=2)
        
        self.assertEqual(formatter.format(234.5678e6), "234567.80 k")
        self.assertEqual(formatter.format(234.5678e3), "234.57 k")
        self.assertEqual(formatter.format(234.5678), "0.23 k")
        self.assertEqual(formatter.format(234.5678e-3), "0.00 k")
        self.assertEqual(formatter.format(234.5678e-6), "0.00 k")
    
    
    def test_suffix(self):
        """Tests whether suffix works correctly."""
        
        # standalone formatter
        formatter = pero.EngFormatter(hide_suffix=True)
        self.assertEqual(formatter.suffix(), "")
        
        self.assertEqual(formatter.format(234.5678e6), "235")
        self.assertEqual(formatter.suffix(), " (M)")
        
        self.assertEqual(formatter.format(234.5678e3), "235")
        self.assertEqual(formatter.suffix(), " (k)")
        
        self.assertEqual(formatter.format(234.5678), "235")
        self.assertEqual(formatter.suffix(), "")
        
        # formatter with domain
        formatter = pero.EngFormatter(hide_suffix=True, domain=1e4)
        self.assertEqual(formatter.suffix(), " (k)")
        
        self.assertEqual(formatter.format(234.5678e6), "234568")
        self.assertEqual(formatter.suffix(), " (k)")
        
        self.assertEqual(formatter.format(234.5678e3), "235")
        self.assertEqual(formatter.suffix(), " (k)")
        
        self.assertEqual(formatter.format(234.5678), "0")
        self.assertEqual(formatter.suffix(), " (k)")
    
    
    def test_convert(self):
        """Tests whether convert works correctly."""
        
        formatter = pero.EngFormatter(domain=1e4)
        
        self.assertEqual(formatter.convert(234.5678e6), 234567.8)
        self.assertEqual(formatter.convert(234.5678e4), 2345.678)
        self.assertEqual(formatter.convert(234.5678), 0.2345678)
        self.assertEqual(formatter.convert(234.5678e-4), 2.345678e-5)
        self.assertEqual(formatter.convert(234.5678e-6), 2.345678e-7)
    
    
    def test_invert(self):
        """Tests whether invert works correctly."""
        
        formatter = pero.EngFormatter(domain=1e4)
        
        self.assertEqual(formatter.invert(234567.8), 234.5678e6)
        self.assertEqual(formatter.invert(2345.678), 234.5678e4)
        self.assertEqual(formatter.invert(0.2345678), 234.5678)
        self.assertEqual(formatter.invert(2.345678e-5), 234.5678e-4)
        self.assertEqual(formatter.invert(2.345678e-7), 234.5678e-6)


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
