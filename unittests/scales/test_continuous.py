#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for Linear scale class."""
    
    
    def test_scale(self):
        """Tests whether scale function works correctly."""
        
        scale = pero.LinScale(
            in_range = (100,500),
            out_range = (10,350))
        
        self.assertEqual(scale.scale(100), 10)
        self.assertEqual(scale.scale(300), 180)
        self.assertEqual(scale.scale(500), 350)
    
    
    def test_invert(self):
        """Tests whether invert function works correctly."""
        
        scale = pero.LinScale(
            in_range = (100,500),
            out_range = (10,350))
        
        self.assertEqual(scale.invert(10), 100)
        self.assertEqual(scale.invert(180), 300)
        self.assertEqual(scale.invert(350), 500)
    
    
    def test_crop(self):
        """Tests whether cropping works correctly."""
        
        scale = pero.LinScale(
            in_range = (100,500),
            out_range = (10,350),
            clip = True)
        
        self.assertEqual(scale.scale(10), 10)
        self.assertEqual(scale.scale(100), 10)
        self.assertEqual(scale.scale(300), 180)
        self.assertEqual(scale.scale(500), 350)
        self.assertEqual(scale.scale(600), 350)
    
    
    def test_no_crop(self):
        """Tests whether cropping works correctly."""
        
        scale = pero.LinScale(
            in_range = (100,500),
            out_range = (10,350),
            clip = False)
        
        self.assertEqual(scale.scale(10), -66.5)
        self.assertEqual(scale.scale(100), 10)
        self.assertEqual(scale.scale(300), 180)
        self.assertEqual(scale.scale(500), 350)
        self.assertEqual(scale.scale(600), 435)
    
    
    def test_arrays(self):
        """Tests whether scale works correctly with arrays."""
        
        scale = pero.LinScale(
            in_range = (100,500),
            out_range = (10,350),
            clip = False)
        
        data = [10, 100, 300, 500, 600]
        model = [-66.5, 10, 180, 350, 435]
        
        self.assertEqual(list(scale.scale(data)), model)
        self.assertEqual(list(scale.invert(model)), data)
        
        scale = pero.LinScale(
            in_range = (100,500),
            out_range = (10,350),
            clip = True)
        
        data = [10, 100, 300, 500, 600]
        model = [10, 10, 180, 350, 350]
        model2 = [100, 100, 300, 350, 350]
        
        self.assertEqual(list(scale.scale(data)), model)
        self.assertEqual(list(scale.invert(model)), model2)


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
