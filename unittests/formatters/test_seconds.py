#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for seconds formatter."""
    
    
    def test_standalone(self):
        """Tests whether formatter works as standalone tool."""
        
        formatter = pero.SecondsFormatter()
        
        # test days
        self.assertEqual(formatter.format(24*60*60), "1 d")
        self.assertEqual(formatter.format(24*60*60 + 30*60), "1 d")
        
        # test hours
        self.assertEqual(formatter.format(60*60), "1 h")
        self.assertEqual(formatter.format(24*60*60 - 1), "24 h")
        
        # test minutes
        self.assertEqual(formatter.format(60), "1 m")
        self.assertEqual(formatter.format(60*60 - 1), "60 m")
        
        # test seconds
        self.assertEqual(formatter.format(1), "1 s")
        self.assertEqual(formatter.format(60-1), "59 s")
        
        # test milliseconds
        self.assertEqual(formatter.format(1e-3), "1 ms")
        self.assertEqual(formatter.format(1-0.1), "900 ms")
        
        # test microseconds
        self.assertEqual(formatter.format(1e-6), "1 us")
        self.assertEqual(formatter.format(1e-3-1e-4), "900 us")
    
    
    def test_places(self):
        """Tests whether places works correctly."""
        
        formatter = pero.SecondsFormatter(places=0)
        
        self.assertEqual(formatter.format(60*60 + 30*60), "2 h")
        self.assertEqual(formatter.format(70.5), "1 m")
        self.assertEqual(formatter.format(17.567), "18 s")
        self.assertEqual(formatter.format(.1), "100 ms")
        
        formatter = pero.SecondsFormatter(places=2)
        
        self.assertEqual(formatter.format(60*60 + 30*60), "1.50 h")
        self.assertEqual(formatter.format(70.5), "1.18 m")
        self.assertEqual(formatter.format(17.567), "17.57 s")
        self.assertEqual(formatter.format(.1), "100.00 ms")
    
    
    def test_precision(self):
        """Tests whether precision works correctly."""
        
        formatter = pero.SecondsFormatter(precision=60*60)
        
        self.assertEqual(formatter.format(60*60 + 30*60 - 1), "1 h")
        self.assertEqual(formatter.format(70.5), "1 m")
        self.assertEqual(formatter.format(17.567), "18 s")
        self.assertEqual(formatter.format(.1), "100 ms")
        
        formatter = pero.SecondsFormatter(precision=60)
        
        self.assertEqual(formatter.format(60*60 + 30*60 - 1), "1.50 h")
        self.assertEqual(formatter.format(70.5), "1 m")
        self.assertEqual(formatter.format(17.567), "18 s")
        self.assertEqual(formatter.format(.1), "100 ms")
    
    
    def test_domain(self):
        """Tests whether domain works correctly."""
        
        formatter = pero.SecondsFormatter(domain=60*60)
        
        self.assertEqual(formatter.format(60*60 + 30*60 - 1), "1 h")
        self.assertEqual(formatter.format(70.5), "0 h")
        self.assertEqual(formatter.format(17.567), "0 h")
        self.assertEqual(formatter.format(.1), "0 h")
        
        formatter = pero.SecondsFormatter(domain=60)
        
        self.assertEqual(formatter.format(60*60 + 30*60 - 1), "90 m")
        self.assertEqual(formatter.format(70.5), "1 m")
        self.assertEqual(formatter.format(17.567), "0 m")
        self.assertEqual(formatter.format(.1), "0 m")
    
    
    def test_digits(self):
        """Tests whether digits works correctly."""
        
        # check domain and precision
        formatter = pero.SecondsFormatter(domain=60*60, precision=60)
        
        self.assertEqual(formatter.format(60*60 + 30*60 - 1), "1.50 h")
        self.assertEqual(formatter.format(70.5), "0.02 h")
        self.assertEqual(formatter.format(17.567), "0.00 h")
        self.assertEqual(formatter.format(.1), "0.00 h")
        
        formatter = pero.SecondsFormatter(domain=60*4, precision=30)
        
        self.assertEqual(formatter.format(60*60 + 30*60 - 1), "90.0 m")
        self.assertEqual(formatter.format(70.5), "1.2 m")
        self.assertEqual(formatter.format(17.567), "0.3 m")
        self.assertEqual(formatter.format(.1), "0.0 m")
        
        # check domain, precision and places
        formatter = pero.SecondsFormatter(domain=60*60, precision=60, places=1)
        
        self.assertEqual(formatter.format(60*60 + 30*60 - 1), "1.5 h")
        self.assertEqual(formatter.format(70.5), "0.0 h")
        self.assertEqual(formatter.format(17.567), "0.0 h")
        self.assertEqual(formatter.format(.1), "0.0 h")
    
    
    def test_suffix(self):
        """Tests whether suffix works correctly."""
        
        # standalone formatter
        formatter = pero.SecondsFormatter(hide_suffix=True)
        self.assertEqual(formatter.suffix(), "")
        
        self.assertEqual(formatter.format(60*60), "1")
        self.assertEqual(formatter.suffix(), " (h)")
        
        self.assertEqual(formatter.format(60), "1")
        self.assertEqual(formatter.suffix(), " (m)")
        
        self.assertEqual(formatter.format(59), "59")
        self.assertEqual(formatter.suffix(), " (s)")
        
        # formatter with domain
        formatter = pero.SecondsFormatter(hide_suffix=True, domain=60)
        self.assertEqual(formatter.suffix(), " (m)")
        
        self.assertEqual(formatter.format(60*60), "60")
        self.assertEqual(formatter.suffix(), " (m)")
        
        self.assertEqual(formatter.format(60), "1")
        self.assertEqual(formatter.suffix(), " (m)")
        
        self.assertEqual(formatter.format(59), "1")
        self.assertEqual(formatter.suffix(), " (m)")
        
        self.assertEqual(formatter.format(25), "0")
        self.assertEqual(formatter.suffix(), " (m)")
    
    
    def test_convert(self):
        """Tests whether convert works correctly."""
        
        formatter = pero.SecondsFormatter(domain=60)
        
        self.assertEqual(formatter.convert(60*60), 60)
        self.assertEqual(formatter.convert(60), 1)
        self.assertEqual(formatter.convert(30), 0.5)
        self.assertEqual(formatter.convert(15), 0.25)
        self.assertEqual(formatter.convert(0.6), 0.01)
    
    
    def test_invert(self):
        """Tests whether invert works correctly."""
        
        formatter = pero.SecondsFormatter(domain=60)
        
        self.assertEqual(formatter.invert(60), 60*60)
        self.assertEqual(formatter.invert(1), 60)
        self.assertEqual(formatter.invert(0.5), 30)
        self.assertEqual(formatter.invert(0.25), 15)
        self.assertEqual(formatter.invert(0.01), 0.6)


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
