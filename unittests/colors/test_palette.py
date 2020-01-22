#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for Palette class."""
    
    
    def test_constructor(self):
        """Tests whether constructor works correctly."""
        
        color0 = pero.Color.Red
        color1 = pero.Color(100, 150, 200)
        color2 = "#aaa"
        
        palette = pero.Palette((color0, color1, color2))
    
    
    def test_getitem(self):
        """Tests whether colors are accessed correctly."""
        
        color0 = pero.Color.Red
        color1 = pero.Color.Green
        color2 = pero.Color.Blue
        
        palette = pero.Palette((color0, color1, color2))
        
        self.assertTrue(palette[0] is color0)
        self.assertTrue(palette[1] is color1)
        self.assertTrue(palette[2] is color2)
    
    
    def test_reversed(self):
        """Tests whether reversed palette is correctly created from parent."""
        
        color0 = pero.Color.Red
        color1 = pero.Color.Green
        color2 = pero.Color.Blue
        color3 = pero.Color.Cyan
        color4 = pero.Color.Magenta
        color5 = pero.Color.Yellow
        
        colors = (color0, color1, color2, color3, color4, color5)
        palette = pero.Palette(colors)
        
        rev = palette.reversed("Reversed")
        
        self.assertEqual(rev.name, "Reversed")
        self.assertEqual(len(rev), len(palette))
        
        self.assertTrue(rev[0] is palette[5])
        self.assertTrue(rev[1] is palette[4])
        self.assertTrue(rev[2] is palette[3])
        self.assertTrue(rev[3] is palette[2])
        self.assertTrue(rev[4] is palette[1])
        self.assertTrue(rev[5] is palette[0])
    
    
    def test_from_name(self):
        """Tests whether named palettes can be accessed."""
        
        # test from name
        palette = pero.Palette.from_name('Spectral')
        palette = pero.Palette.from_name('spectral')
        
        # test from class
        palette = pero.Palette.Spectral
        palette = pero.Palette.spectral
        
        # test from lib
        palette = pero.PALETTES.Spectral
        palette = pero.PALETTES.spectral
        
        # test from module
        palette = pero.colors.Spectral
    
    
    def test_from_palette(self):
        """Tests whether new palette is correctly created from parent."""
        
        color0 = pero.Color.Red
        color1 = pero.Color.Green
        color2 = pero.Color.Blue
        color3 = pero.Color.Cyan
        color4 = pero.Color.Magenta
        color5 = pero.Color.Yellow
        color6 = pero.Color.Black
        
        colors = (color0, color1, color2, color3, color4, color5, color6)
        palette = pero.Palette(colors)
        
        picked = pero.Palette.from_palette(palette, 2)
        self.assertEqual(len(picked), 2)
        self.assertTrue(picked[0] is color0)
        self.assertTrue(picked[1] is color6)
        
        picked = pero.Palette.from_palette(palette, 3)
        self.assertEqual(len(picked), 3)
        self.assertTrue(picked[0] is color0)
        self.assertTrue(picked[1] is color3)
        self.assertTrue(picked[2] is color6)
        
        picked = pero.Palette.from_palette(palette, 4)
        self.assertEqual(len(picked), 4)
        self.assertTrue(picked[0] is color0)
        self.assertTrue(picked[1] is color2)
        self.assertTrue(picked[2] is color4)
        self.assertTrue(picked[3] is color6)
    
    
    def test_from_gradient(self):
        """Tests whether new palette is correctly created from gradient."""
        
        color0 = pero.Color.Black
        color1 = pero.Color.White
        
        colors = (color0, color1)
        gradient = pero.Gradient(colors)
        
        picked = pero.Palette.from_gradient(gradient, 2)
        self.assertEqual(len(picked), 2)
        self.assertEqual(picked[0], color0)
        self.assertEqual(picked[1], color1)
        
        picked = pero.Palette.from_gradient(gradient, 3)
        self.assertEqual(len(picked), 3)
        self.assertEqual(picked[0], color0)
        self.assertEqual(picked[1], (128, 128, 128))
        self.assertEqual(picked[2], color1)
        
        picked = pero.Palette.from_gradient(gradient, 4)
        self.assertEqual(len(picked), 4)
        self.assertEqual(picked[0], color0)
        self.assertEqual(picked[1], (85, 85, 85))
        self.assertEqual(picked[2], (170, 170, 170))
        self.assertEqual(picked[3], color1)
    
    
    def test_name_registering(self):
        """Tests whether new named palettes are registered."""
        
        # init named palette
        colors = (pero.Color.Red, pero.Color.Green, pero.Color.Blue)
        model = pero.Palette(colors, "MyPalette")
        
        # test from name
        palette = pero.Palette.from_name('MyPalette')
        self.assertTrue(palette is model)
        
        palette = pero.Palette.from_name('mypalette')
        self.assertTrue(palette is model)
        
        # test from class
        palette = pero.Palette.MyPalette
        self.assertTrue(palette is model)
        
        palette = pero.Palette.mypalette
        self.assertTrue(palette is model)
        
        # test from lib
        palette = pero.PALETTES.MyPalette
        self.assertTrue(palette is model)
        
        palette = pero.PALETTES.mypalette
        self.assertTrue(palette is model)


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
