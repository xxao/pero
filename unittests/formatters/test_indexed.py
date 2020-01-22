#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for custom function formatter."""
    
    
    def test_exact(self):
        """Tests whether formatter works for exact indices."""
        
        labels = ('zero', 'one', 'two', 'three', 'four')
        formatter = pero.IndexFormatter(labels=labels)
        
        self.assertEqual(formatter.format(0), 'zero')
        self.assertEqual(formatter.format(1), 'one')
        self.assertEqual(formatter.format(2), 'two')
        self.assertEqual(formatter.format(3), 'three')
        self.assertEqual(formatter.format(4), 'four')
    
    
    def test_rounding(self):
        """Tests whether formatter works for floats."""
        
        labels = ('zero', 'one', 'two', 'three', 'four')
        formatter = pero.IndexFormatter(labels=labels, default=pero.UNDEF)
        
        self.assertEqual(formatter.format(2.2), 'two')
        self.assertEqual(formatter.format(2.7), 'three')
        self.assertEqual(formatter.format(4.6), pero.UNDEF)
    
    
    def test_outside(self):
        """Tests whether formatter works for outside indices."""
        
        labels = ('zero', 'one', 'two', 'three', 'four')
        formatter = pero.IndexFormatter(labels=labels, default=pero.UNDEF)
        
        self.assertEqual(formatter.format(-1), pero.UNDEF)
        self.assertEqual(formatter.format(5), pero.UNDEF)
    
    
    def test_default(self):
        """Tests whether default value works correctly."""
        
        labels = ('zero', 'one', 'two', 'three', 'four')
        formatter = pero.IndexFormatter(labels=labels, default='joker')
        
        self.assertEqual(formatter.format(-1), 'joker')
        self.assertEqual(formatter.format(5), 'joker')


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
