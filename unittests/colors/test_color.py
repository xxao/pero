#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for Color class."""
    
    
    def test_valid_constructor(self):
        """Tests whether constructor works correctly."""
        
        # test individual channels
        color = pero.Color(100, 150, 200, 10)
        
        self.assertEqual(color.red, 100)
        self.assertEqual(color.green, 150)
        self.assertEqual(color.blue, 200)
        self.assertEqual(color.alpha, 10)
        
        color = pero.Color(100, 150, 200)
        
        self.assertEqual(color.red, 100)
        self.assertEqual(color.green, 150)
        self.assertEqual(color.blue, 200)
        self.assertEqual(color.alpha, 255)
        
        # test tuple
        color = pero.Color((100, 150, 200, 10))
        
        self.assertEqual(color.red, 100)
        self.assertEqual(color.green, 150)
        self.assertEqual(color.blue, 200)
        self.assertEqual(color.alpha, 10)
        
        color = pero.Color((100, 150, 200))
        
        self.assertEqual(color.red, 100)
        self.assertEqual(color.green, 150)
        self.assertEqual(color.blue, 200)
        self.assertEqual(color.alpha, 255)
        
        # test hex
        color = pero.Color("#6496c80a")
        
        self.assertEqual(color.red, 100)
        self.assertEqual(color.green, 150)
        self.assertEqual(color.blue, 200)
        self.assertEqual(color.alpha, 10)
        
        color = pero.Color("#6496c8")
        
        self.assertEqual(color.red, 100)
        self.assertEqual(color.green, 150)
        self.assertEqual(color.blue, 200)
        self.assertEqual(color.alpha, 255)
    
    
    def test_invalid_constructor(self):
        """Tests whether constructor works correctly."""
        
        # test incorrect type
        with self.assertRaises(ValueError):
            color = pero.Color("red", 150, 200, 10)
        with self.assertRaises(ValueError):
            color = pero.Color(100, "green", 200, 10)
        with self.assertRaises(ValueError):
            color = pero.Color(100, 150, "blue", 100)
        with self.assertRaises(ValueError):
            color = pero.Color(100, 150, 200, "alpha")
        
        # test incorrect values
        with self.assertRaises(ValueError):
            color = pero.Color(300, 150, 200, 10)
        with self.assertRaises(ValueError):
            color = pero.Color(100, 300, 200, 10)
        with self.assertRaises(ValueError):
            color = pero.Color(100, 150, 300, 100)
        with self.assertRaises(ValueError):
            color = pero.Color(100, 150, 200, 300)
        with self.assertRaises(ValueError):
            color = pero.Color(-1, 150, 200, 10)
        with self.assertRaises(ValueError):
            color = pero.Color(100, -1, 200, 10)
        with self.assertRaises(ValueError):
            color = pero.Color(100, 150, -1, 100)
        with self.assertRaises(ValueError):
            color = pero.Color(100, 150, 200, -1)
    
    
    def test_equals(self):
        """Tests whether equality comparer works correctly."""
        
        # test full equal
        c1 = pero.Color(100, 150, 200, 255, name="Name")
        c2 = pero.Color(100, 150, 200, 255, name="Name")
        
        self.assertEqual(c1, c2)
        self.assertEqual(c1, c2.rgba)
        
        # test equal channels
        c1 = pero.Color(100, 150, 200, 255, name="Name1")
        c2 = pero.Color(100, 150, 200, 255, name="Name2")
        
        self.assertEqual(c1, c2)
        self.assertEqual(c1, c2.rgba)
        
        # test non-equal channels
        c1 = pero.Color(101, 150, 200, 255)
        c2 = pero.Color(100, 150, 200, 255)
        
        self.assertNotEqual(c1, c2)
        self.assertNotEqual(c1, c2.rgba)
        
        c1 = pero.Color(100, 151, 200, 255)
        c2 = pero.Color(100, 150, 200, 255)
        
        self.assertNotEqual(c1, c2)
        self.assertNotEqual(c1, c2.rgba)
        
        c1 = pero.Color(100, 150, 201, 255)
        c2 = pero.Color(100, 150, 200, 255)
        
        self.assertNotEqual(c1, c2)
        self.assertNotEqual(c1, c2.rgba)
        
        c1 = pero.Color(100, 150, 201, 251)
        c2 = pero.Color(100, 150, 200, 255)
        
        self.assertNotEqual(c1, c2)
        self.assertNotEqual(c1, c2.rgba)
    
    
    def test_rgba(self):
        """Tests whether RGBA channels are returned correctly."""
        
        color = pero.Color(100, 150, 200, 250)
        self.assertEqual(color.rgba, (100, 150, 200, 250))
        
        color = pero.Color(100, 150, 200, 250)
        self.assertEqual(color.rgba_r, (100/255, 150/255, 200/255, 250/255))
        
        color = pero.Color(100, 150, 200, 250)
        self.assertEqual(color.rgb, (100, 150, 200))
        
        color = pero.Color(100, 150, 200, 250)
        self.assertEqual(color.rgb_r, (100/255, 150/255, 200/255))
    
    
    def test_hex(self):
        """Tests whether RGBA hex is returned correctly."""
        
        color = pero.Color(0, 150, 200, 250)
        self.assertEqual(color.hex, "#0096c8fa")
    
    
    def test_lighter(self):
        """Tests whether making lighter color works correctly."""
        
        color = pero.Color(50, 100, 180, 200)
        
        lighter = color.lighter(0)
        self.assertEqual(lighter.rgba, (50, 100, 180, 200))
        
        lighter = color.lighter(0.5)
        self.assertEqual(lighter.rgba, (153, 178, 218, 200))
        
        lighter = color.lighter(1)
        self.assertEqual(lighter.rgba, (255, 255, 255, 200))
        
        # test incorrect value
        with self.assertRaises(ValueError):
            trans = color.lighter(-1)
        
        with self.assertRaises(ValueError):
            trans = color.lighter(2)
    
    
    def test_darker(self):
        """Tests whether making darker color works correctly."""
        
        color = pero.Color(152, 177, 217, 200)
        
        darker = color.darker(0)
        self.assertEqual(darker.rgba, (152, 177, 217, 200))
        
        darker = color.darker(0.5)
        self.assertEqual(darker.rgba, (76, 89, 109, 200))
        
        darker = color.darker(1)
        self.assertEqual(darker.rgba, (0, 0, 0, 200))
        
        # test incorrect value
        with self.assertRaises(ValueError):
            trans = color.darker(-1)
        
        with self.assertRaises(ValueError):
            trans = color.darker(2)
    
    
    def test_opaque(self):
        """Tests whether making opaque color works correctly."""
        
        color = pero.Color(152, 177, 217, 200)
        
        trans = color.opaque(0)
        self.assertEqual(trans.rgba, (152, 177, 217, 0))
        
        trans = color.opaque(1)
        self.assertEqual(trans.rgba, (152, 177, 217, 255))
        
        trans = color.opaque(0.5)
        self.assertEqual(trans.rgba, (152, 177, 217, 128))
        
        # test incorrect value
        with self.assertRaises(ValueError):
            trans = color.opaque(-1)
        
        with self.assertRaises(ValueError):
            trans = color.opaque(2)
    
    
    def test_trans(self):
        """Tests whether making transparent color works correctly."""
        
        color = pero.Color(152, 177, 217, 200)
        
        trans = color.trans(0)
        self.assertEqual(trans.rgba, (152, 177, 217, 255))
        
        trans = color.trans(1)
        self.assertEqual(trans.rgba, (152, 177, 217, 0))
        
        trans = color.trans(0.5)
        self.assertEqual(trans.rgba, (152, 177, 217, 128))
        
        # test incorrect value
        with self.assertRaises(ValueError):
            trans = color.trans(-1)
        
        with self.assertRaises(ValueError):
            trans = color.trans(2)
    
    
    def test_interpolate(self):
        """Tests whether interpolation works correctly."""
        
        c1 = pero.Color(50, 100, 150, 200)
        c2 = pero.Color(100, 150, 200, 250)
        
        inter = pero.Color.interpolate(c1, c2, 0.5)
        self.assertEqual(inter.rgba, (75, 125, 175, 225))
        
        inter = pero.Color.interpolate(c1, c2, -0.5)
        self.assertEqual(inter.rgba, (25, 75, 125, 175))
        
        inter = pero.Color.interpolate(c1, c2, -1000)
        self.assertEqual(inter.rgba, (0, 0, 0, 0))
        
        inter = pero.Color.interpolate(c1, c2, 1.5)
        self.assertEqual(inter.rgba, (125, 175, 225, 255))
        
        inter = pero.Color.interpolate(c1, c2, 1000)
        self.assertEqual(inter.rgba, (255, 255, 255, 255))
    
    
    def test_create(self):
        """Tests whether create method works correctly."""
        
        # test from color
        color = pero.Color.create(pero.Color(255, 0, 0, 255))
        self.assertEqual(color.rgba, (255, 0, 0, 255))
        
        # test from name
        color = pero.Color.create('Red')
        self.assertEqual(color.rgba, (255, 0, 0, 255))
        
        # test from tuple
        color = pero.Color.create((170, 187, 204, 221))
        self.assertEqual(color.rgba, (170, 187, 204, 221))
        
        # test from hex
        color = pero.Color.create("#aabbccdd")
        self.assertEqual(color.rgba, (170, 187, 204, 221))
    
    
    def test_from_name(self):
        """Tests whether named colors can be accessed."""
        
        # test from name
        color = pero.Color.from_name('Red')
        color = pero.Color.from_name('red')
        
        # test from class
        color = pero.Color.Red
        color = pero.Color.red
        
        # test from lib
        color = pero.COLORS.Red
        color = pero.COLORS.red
        
        # test from module
        color = pero.colors.Red
    
    
    def test_from_hex(self):
        """Tests whether color is correctly created from hex."""
        
        # test all channels
        color = pero.Color("#aabbccdd")
        self.assertEqual(color.rgba, (170, 187, 204, 221))
        
        color = pero.Color("#abcd")
        self.assertEqual(color.rgba, (170, 187, 204, 221))
        
        # test without alpha
        color = pero.Color("#aabbcc")
        self.assertEqual(color.rgba, (170, 187, 204, 255))
        
        color = pero.Color("#abc")
        self.assertEqual(color.rgba, (170, 187, 204, 255))
    
    
    def test_name_registering(self):
        """Tests whether new named colors are registered."""
        
        # init named color
        model = pero.Color(0, 0, 0, 0, name="MyTransparent")
        
        # test from name
        color = pero.Color.from_name('MyTransparent')
        self.assertTrue(color is model)
        
        color = pero.Color.from_name('mytransparent')
        self.assertTrue(color is model)
        
        # test from class
        color = pero.Color.MyTransparent
        self.assertTrue(color is model)
        
        color = pero.Color.mytransparent
        self.assertTrue(color is model)
        
        # test from lib
        color = pero.COLORS.MyTransparent
        self.assertTrue(color is model)
        
        color = pero.COLORS.mytransparent
        self.assertTrue(color is model)


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
