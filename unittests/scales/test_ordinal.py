#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for ordinal scale."""
    
    
    def test_scale(self):
        """Tests whether scale works correctly."""
        
        in_range = [1, 2, 3]
        out_range = ["red", "green", "blue"]
        
        scale = pero.OrdinalScale(
            in_range = in_range,
            out_range = out_range)
        
        self.assertEqual(scale.scale(1), "red")
        self.assertEqual(scale.scale(2), "green")
        self.assertEqual(scale.scale(3), "blue")
    
    
    def test_invert(self):
        """Tests whether invert works correctly."""
        
        in_range = [1, 2, 3]
        out_range = ["red", "green", "blue"]
        
        scale = pero.OrdinalScale(
            in_range = in_range,
            out_range = out_range)
        
        # check scale
        self.assertEqual(scale.invert("red"), 1)
        self.assertEqual(scale.invert("green"), 2)
        self.assertEqual(scale.invert("blue"), 3)
    
    
    def test_default(self):
        """Tests whether default value works correctly."""
        
        in_range = [1, 2, 3]
        out_range = ["red", "green", "blue"]
        default = "black"
        
        scale = pero.OrdinalScale(
            in_range = in_range,
            out_range = out_range,
            default = default)
        
        self.assertEqual(scale.scale(0), "black")
        self.assertEqual(scale.invert("black"), None)
    
    
    def test_implicit(self):
        """Tests whether implicit values work correctly."""
        
        out_range = ["red", "green", "blue"]
        default = None
        
        # disable implicit
        scale = pero.OrdinalScale(
            out_range = out_range,
            default = default,
            implicit = False)
        
        self.assertEqual(scale.scale(1), None)
        self.assertEqual(scale.invert("red"), None)
        
        # enable implicit
        scale = pero.OrdinalScale(
            out_range = out_range,
            default = default,
            implicit = True)
        
        self.assertEqual(scale.scale(1), "red")
        self.assertEqual(scale.scale(2), "green")
        self.assertEqual(scale.scale(1), "red")
        self.assertEqual(scale.scale(3), "blue")
        
        self.assertEqual(scale.invert("red"), 1)
        self.assertEqual(scale.invert("green"), 2)
        self.assertEqual(scale.invert("blue"), 3)
    
    
    def test_recycle(self):
        """Tests whether recycling works correctly."""
        
        in_range = [1, 2, 3, 4, 5, 6, 7]
        out_range = ["red", "green", "blue"]
        default = None
        
        # disable recycling
        scale = pero.OrdinalScale(
            in_range = in_range,
            out_range = out_range,
            default = default,
            recycle = False)
        
        self.assertEqual(scale.scale(1), "red")
        self.assertEqual(scale.scale(7), None)
        self.assertEqual(scale.invert("red"), 1)
        
        # enable recycling
        scale = pero.OrdinalScale(
            in_range = in_range,
            out_range = out_range,
            default = default,
            recycle = True)
        
        self.assertEqual(scale.scale(1), "red")
        self.assertEqual(scale.scale(4), "red")
        self.assertEqual(scale.scale(5), "green")
        self.assertEqual(scale.scale(6), "blue")
        self.assertEqual(scale.scale(7), "red")
        
        self.assertEqual(scale.invert("red"), 1)
        self.assertEqual(scale.invert("green"), 2)
        self.assertEqual(scale.invert("blue"), 3)


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
