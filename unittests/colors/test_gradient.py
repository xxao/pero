#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for Gradient class."""
    
    
    def test_constructor(self):
        """Tests whether constructor works correctly."""
        
        # full specification
        colors = (pero.Color.Red, pero.Color.Green, pero.Color.Blue)
        stops = (0, 0.5, 1)
        gradient = pero.Gradient(colors, stops, "Name")
        
        self.assertEqual(gradient.colors, colors)
        self.assertEqual(gradient.stops, stops)
        self.assertEqual(gradient.name, "Name")
        
        # no name
        colors = (pero.Color.Red, pero.Color.Green, pero.Color.Blue)
        stops = (0, 0.5, 1)
        gradient = pero.Gradient(colors, stops)
        
        self.assertEqual(gradient.colors, colors)
        self.assertEqual(gradient.stops, stops)
        self.assertEqual(gradient.name, None)
        
        # no stops
        colors = (pero.Color.Red, pero.Color.Green, pero.Color.Blue)
        stops = (0, 0.5, 1)
        gradient = pero.Gradient(colors)
        
        self.assertEqual(gradient.colors, colors)
        self.assertEqual(gradient.stops, stops)
        self.assertEqual(gradient.name, None)
        
        # stops range
        colors = (pero.Color.Red, pero.Color.Green, pero.Color.Blue)
        stops = (100, 150, 200)
        gradient = pero.Gradient(colors, (100, 200))
        
        self.assertEqual(gradient.colors, colors)
        self.assertEqual(gradient.stops, stops)
        self.assertEqual(gradient.name, None)
        
        # test invalid color
        colors = (pero.Color.Red, pero.Color.Green, "blue", 0)
        
        with self.assertRaises(ValueError):
            gradient = pero.Gradient(colors)
        
        # test invalid stop
        colors = (pero.Color.Red, pero.Color.Green, pero.Color.Blue)
        stops = (0, 0.5, "1")
        
        with self.assertRaises(TypeError):
            gradient = pero.Gradient(colors, stops)
        
        # test unsorted stops
        colors = (pero.Color.Red, pero.Color.Green, pero.Color.Blue)
        stops = (0, 1, 0.5)
        
        with self.assertRaises(ValueError):
            gradient = pero.Gradient(colors, stops)
        
        # test unequal size
        colors = (pero.Color.Red, pero.Color.Green, pero.Color.Blue)
        stops = (0, 0.25, 0.5, 0.75, 1)
        
        with self.assertRaises(ValueError):
            gradient = pero.Gradient(colors, stops)
    
    
    def test_color_at(self):
        """Tests whether gradient color is generated correctly."""
        
        # init gradient
        colors = (pero.Color.Red, pero.Color.Green, pero.Color.Blue)
        stops = (0, 0.5, 1)
        gradient = pero.Gradient(colors, stops, "Name")
        
        # test below range
        color = gradient.color_at(-1)
        self.assertEqual(color, colors[0])
        
        # test above range
        color = gradient.color_at(2)
        self.assertEqual(color, colors[-1])
        
        # test first
        color = gradient.color_at(0)
        self.assertEqual(color, colors[0])
        
        # test middle
        color = gradient.color_at(0.5)
        self.assertEqual(color, colors[1])
        
        # test last
        color = gradient.color_at(1)
        self.assertEqual(color, colors[-1])
        
        # test interpolated
        color = gradient.color_at(0.25)
        model = pero.Color(128,64,0,255)
        self.assertEqual(color, model)
    
    
    def test_normalized(self):
        """Tests whether gradient normalization works correctly."""
        
        # init gradient
        colors = (pero.Color.Red, pero.Color.Green, pero.Color.Blue)
        stops = (10, 60, 110)
        gradient = pero.Gradient(colors, stops)
        
        # test normalized
        normalized = gradient.normalized()
        model = (0, .5, 1)
        self.assertEqual(normalized.stops, model)
        
        normalized = gradient.normalized(0, 1)
        model = (0, .5, 1)
        self.assertEqual(normalized.stops, model)
        
        normalized = gradient.normalized(100, 1100)
        model = (100, 600, 1100)
        self.assertEqual(normalized.stops, model)
    
    
    def test_from_name(self):
        """Tests whether named gradients can be accessed."""
        
        # init named gradient
        colors = (pero.Color.Red, pero.Color.Green, pero.Color.Blue)
        model = pero.Gradient(colors, name="MyGradient")
        
        # test from name
        gradient = pero.Gradient.from_name('MyGradient')
        gradient = pero.Gradient.from_name('mygradient')
        
        # test from palette name
        gradient = pero.Gradient.from_name('Spectral')
        gradient = pero.Gradient.from_name('spectral')
    
    
    def test_name_registering(self):
        """Tests whether new named gradients are registered."""
        
        # init named gradient
        colors = (pero.Color.Red, pero.Color.Green, pero.Color.Blue)
        model = pero.Gradient(colors, name="MyGradient")
        
        # test from class
        gradient = pero.Gradient.MyGradient
        self.assertTrue(gradient is model)
        
        gradient = pero.Gradient.mygradient
        self.assertTrue(gradient is model)
        
        # test from lib
        gradient = pero.GRADIENTS.MyGradient
        self.assertTrue(gradient is model)
        
        gradient = pero.GRADIENTS.mygradient
        self.assertTrue(gradient is model)


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
