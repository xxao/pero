#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for stringed formatter."""
    
    
    def test_empty_formatter(self):
        """Tests whether formatter works as standalone tool."""
        
        formatter = pero.EmptyFormatter()
        
        self.assertEqual(formatter.format(0), "")
        self.assertEqual(formatter.format(1), "")
        self.assertEqual(formatter.format(1e6), "")
    
    
    def test_str_formatter(self):
        """Tests whether formatter works as standalone tool."""
        
        formatter = pero.StrFormatter(template="{:.2f} u")
        
        self.assertEqual(formatter.format(0), "0.00 u")
        self.assertEqual(formatter.format(1.5), "1.50 u")
        self.assertEqual(formatter.format(1e6), "1000000.00 u")
    
    
    def test_str_formatter_trim(self):
        """Tests whether formatter work with auto trimming."""
        
        formatter = pero.StrFormatter(template="\n{}")
        
        formatter.trim = False
        self.assertEqual(formatter.format("test"), "\ntest")
        
        formatter.trim = True
        self.assertEqual(formatter.format("test"), "test")
    
    
    def test_printf_formatter(self):
        """Tests whether formatter works as standalone tool."""
        
        formatter = pero.PrintfFormatter(template="%0.2f u")
        
        self.assertEqual(formatter.format(0), "0.00 u")
        self.assertEqual(formatter.format(1.5), "1.50 u")
        self.assertEqual(formatter.format(1e6), "1000000.00 u")
    
    
    def test_printf_formatter_trim(self):
        """Tests whether formatter work with auto trimming."""
        
        formatter = pero.PrintfFormatter(template="\n%s")
        
        formatter.trim = False
        self.assertEqual(formatter.format("test"), "\ntest")
        
        formatter.trim = True
        self.assertEqual(formatter.format("test"), "test")


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
