#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for logarithmic formatter."""
    
    
    def test_normal(self):
        """Tests whether formatter works as standalone tool."""
        
        # test log 10
        formatter = pero.LogFormatter(
            base = 10,
            sci_notation = False,
            exp_notation = False)
        
        self.assertEqual(formatter.format(0), '0')
        self.assertEqual(formatter.format(1.2345e-3), '0.001')
        self.assertEqual(formatter.format(1.2345e1), '10')
        self.assertEqual(formatter.format(1.2345e6), '1000000')
        self.assertEqual(formatter.format(-1.2345e6), '-1000000')
        
        # test log 2
        formatter = pero.LogFormatter(
            base = 2,
            sci_notation = False,
            exp_notation = False)
        
        self.assertEqual(formatter.format(0), '0')
        self.assertEqual(formatter.format(1.2345*2**2), '4')
        self.assertEqual(formatter.format(1.2345*2**3), '8')
        self.assertEqual(formatter.format(1.2345*2**4), '16')
        self.assertEqual(formatter.format(-1.2345*2**4), '-16')
    
    
    def test_sci_notation(self):
        """Tests whether scientific notation works correctly."""
        
        # test log 10
        formatter = pero.LogFormatter(
            base = 10,
            sci_notation = True,
            exp_notation = False)
        
        self.assertEqual(formatter.format(0), '0')
        self.assertEqual(formatter.format(1.2345e-3), '1e-03')
        self.assertEqual(formatter.format(1.2345e1), '1e+01')
        self.assertEqual(formatter.format(1.2345e6), '1e+06')
        self.assertEqual(formatter.format(-1.2345e6), '-1e+06')
        
        # test log 2
        formatter = pero.LogFormatter(
            base = 2,
            sci_notation = True,
            exp_notation = False)
        
        self.assertEqual(formatter.format(0), '0')
        self.assertEqual(formatter.format(1.2345*2**2), '4')
        self.assertEqual(formatter.format(1.2345*2**3), '8')
        self.assertEqual(formatter.format(1.2345*2**4), '16')
        self.assertEqual(formatter.format(-1.2345*2**4), '-16')
    
    
    def test_exp_notation(self):
        """Tests whether exponent notation works correctly."""
        
        # test log 10
        formatter = pero.LogFormatter(
            base = 10,
            sci_notation = False,
            exp_notation = True)
        
        self.assertEqual(formatter.format(0), '0')
        self.assertEqual(formatter.format(1.2345e-3), '10^-3')
        self.assertEqual(formatter.format(1.2345e1), '10^1')
        self.assertEqual(formatter.format(1.2345e6), '10^6')
        self.assertEqual(formatter.format(-1.2345e6), '-10^6')
        
        # test log 2
        formatter = pero.LogFormatter(
            base = 2,
            sci_notation = False,
            exp_notation = True)
        
        self.assertEqual(formatter.format(0), '0')
        self.assertEqual(formatter.format(1.2345*2**2), '2^2')
        self.assertEqual(formatter.format(1.2345*2**3), '2^3')
        self.assertEqual(formatter.format(1.2345*2**4), '2^4')
        self.assertEqual(formatter.format(-1.2345*2**4), '-2^4')


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
