#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for levels scale."""
    
    
    def test_scale_thresholds(self):
        """Tests whether scale works correctly for exact thresholds."""
        
        levels = ["red", "green", "blue"]
        thresholds = [1, 2, 3]
        
        scale = pero.LevelScale(
            in_range = thresholds,
            out_range = levels)
        
        self.assertEqual(scale.scale(1), "red")
        self.assertEqual(scale.scale(2), "green")
        self.assertEqual(scale.scale(3), "blue")
    
    
    def test_scale_inside(self):
        """Tests whether scale works correctly for values inside."""
        
        levels = ["red", "green", "blue"]
        thresholds = [1, 2, 3]
        
        scale = pero.LevelScale(
            in_range = thresholds,
            out_range = levels)
        
        self.assertEqual(scale.scale(1.5), "green")
        self.assertEqual(scale.scale(2.5), "blue")
    
    
    def test_scale_outside(self):
        """Tests whether scale works correctly for values outside."""
        
        levels = ["red", "green", "blue"]
        thresholds = [1, 2, 3]
        
        scale = pero.LevelScale(
            in_range = thresholds,
            out_range = levels)
        
        self.assertEqual(scale.scale(.5), "red")
        self.assertEqual(scale.scale(3.5), None)
    
    
    def test_invert(self):
        """Tests whether invert works correctly."""
        
        levels = ["red", "green", "blue"]
        thresholds = [1, 2, 3]
        
        scale = pero.LevelScale(
            in_range = thresholds,
            out_range = levels)
        
        self.assertEqual(scale.invert("red"), 1)
        self.assertEqual(scale.invert("green"), 2)
        self.assertEqual(scale.invert("blue"), 3)
        self.assertEqual(scale.invert("black"), None)


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
