#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for Linear scale class."""
    
    
    def test_scale(self):
        """Tests whether scale function works correctly."""
        
        scale = pero.LinScale(
            in_range = (100, 500),
            out_range = (10, 350))

        self.assertEqual(scale.scale(50), -32.5)
        self.assertEqual(scale.scale(100), 10)
        self.assertEqual(scale.scale(300), 180)
        self.assertEqual(scale.scale(500), 350)
        self.assertEqual(scale.scale(600), 435)
    
    
    def test_invert(self):
        """Tests whether invert function works correctly."""
        
        scale = pero.LinScale(
            in_range = (100, 500),
            out_range = (10, 350))

        self.assertEqual(scale.invert(-32.5), 50)
        self.assertEqual(scale.invert(10), 100)
        self.assertEqual(scale.invert(180), 300)
        self.assertEqual(scale.invert(350), 500)
        self.assertEqual(scale.invert(435), 600)
    
    
    def test_clip(self):
        """Tests whether clipping works correctly."""
        
        scale = pero.LinScale(
            in_range = (100, 500),
            out_range = (10, 350),
            clip = True)
        
        self.assertEqual(scale.scale(10), 10)
        self.assertEqual(scale.scale(100), 10)
        self.assertEqual(scale.scale(300), 180)
        self.assertEqual(scale.scale(500), 350)
        self.assertEqual(scale.scale(600), 350)

        self.assertEqual(scale.invert(-32.5), 100)
        self.assertEqual(scale.invert(10), 100)
        self.assertEqual(scale.invert(180), 300)
        self.assertEqual(scale.invert(350), 500)
        self.assertEqual(scale.invert(435), 500)
        
        scale = pero.LinScale(
            in_range = (500, 100),
            out_range = (350, 10),
            clip = True)
        
        self.assertEqual(scale.scale(10), 10)
        self.assertEqual(scale.scale(100), 10)
        self.assertEqual(scale.scale(300), 180)
        self.assertEqual(scale.scale(500), 350)
        self.assertEqual(scale.scale(600), 350)

        self.assertEqual(scale.invert(-32.5), 100)
        self.assertEqual(scale.invert(10), 100)
        self.assertEqual(scale.invert(180), 300)
        self.assertEqual(scale.invert(350), 500)
        self.assertEqual(scale.invert(435), 500)
        
        scale = pero.LinScale(
            in_range = (500, 100),
            out_range = (10, 350),
            clip = True)
        
        self.assertEqual(scale.scale(10), 350)
        self.assertEqual(scale.scale(100), 350)
        self.assertEqual(scale.scale(300), 180)
        self.assertEqual(scale.scale(500), 10)
        self.assertEqual(scale.scale(600), 10)

        self.assertEqual(scale.invert(-32.5), 500)
        self.assertEqual(scale.invert(10), 500)
        self.assertEqual(scale.invert(180), 300)
        self.assertEqual(scale.invert(350), 100)
        self.assertEqual(scale.invert(435), 100)
        
        scale = pero.LinScale(
            in_range = (100, 500),
            out_range = (350, 10),
            clip = True)
        
        self.assertEqual(scale.scale(10), 350)
        self.assertEqual(scale.scale(100), 350)
        self.assertEqual(scale.scale(300), 180)
        self.assertEqual(scale.scale(500), 10)
        self.assertEqual(scale.scale(600), 10)

        self.assertEqual(scale.invert(-32.5), 500)
        self.assertEqual(scale.invert(10), 500)
        self.assertEqual(scale.invert(180), 300)
        self.assertEqual(scale.invert(350), 100)
        self.assertEqual(scale.invert(435), 100)
    
    
    def test_arrays(self):
        """Tests whether scale works correctly with arrays."""
        
        scale = pero.LinScale(
            in_range = (100, 500),
            out_range = (10, 350))
        
        data = [50, 100, 300, 500, 600]
        model = [-32.5, 10, 180, 350, 435]
        
        self.assertEqual(list(scale.scale(data)), model)
        self.assertEqual(list(scale.invert(model)), data)
    
    
    def test_arrays_clip(self):
        """Tests whether scale clipping works correctly with arrays."""
        
        scale = pero.LinScale(
            in_range = (100, 500),
            out_range = (10, 350),
            clip = True)
        
        data = [10, 100, 300, 500, 600]
        model = [10, 10, 180, 350, 350]
        self.assertEqual(list(scale.scale(data)), model)
        
        data = [-32.5, 10, 180, 350, 435]
        model = [100, 100, 300, 500, 500]
        self.assertEqual(list(scale.invert(data)), model)
        
        scale = pero.LinScale(
            in_range = (500, 100),
            out_range = (350, 10),
            clip = True)
        
        data = [10, 100, 300, 500, 600]
        model = [10, 10, 180, 350, 350]
        self.assertEqual(list(scale.scale(data)), model)
        
        data = [-32.5, 10, 180, 350, 435]
        model = [100, 100, 300, 500, 500]
        self.assertEqual(list(scale.invert(data)), model)
        
        scale = pero.LinScale(
            in_range = (500, 100),
            out_range = (10, 350),
            clip = True)
        
        data = [10, 100, 300, 500, 600]
        model = [350, 350, 180, 10, 10]
        self.assertEqual(list(scale.scale(data)), model)
        
        data = [-32.5, 10, 180, 350, 435]
        model = [500, 500, 300, 100, 100]
        self.assertEqual(list(scale.invert(data)), model)
        
        scale = pero.LinScale(
            in_range = (100, 500),
            out_range = (350, 10),
            clip = True)
        
        data = [10, 100, 300, 500, 600]
        model = [350, 350, 180, 10, 10]
        self.assertEqual(list(scale.scale(data)), model)
        
        data = [-32.5, 10, 180, 350, 435]
        model = [500, 500, 300, 100, 100]
        self.assertEqual(list(scale.invert(data)), model)


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
