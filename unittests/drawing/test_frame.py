#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for Frame class."""
    
    
    def test_init(self):
        """Tests whether constructor works correctly."""
        
        frame = pero.Frame(10, 20, 100, 200)
        
        self.assertEqual(frame.x, 10)
        self.assertEqual(frame.y, 20)
        self.assertEqual(frame.width, 100)
        self.assertEqual(frame.height, 200)
        
        self.assertEqual(frame.x1, 10)
        self.assertEqual(frame.y1, 20)
        self.assertEqual(frame.x2, 110)
        self.assertEqual(frame.y2, 220)
        
        self.assertEqual(frame.cx, 60)
        self.assertEqual(frame.cy, 120)
        
        self.assertEqual(frame.tl, (10, 20))
        self.assertEqual(frame.tr, (110, 20))
        self.assertEqual(frame.bl, (10, 220))
        self.assertEqual(frame.br, (110, 220))
        self.assertEqual(frame.c, (60, 120))
        
        self.assertEqual(frame.w, 100)
        self.assertEqual(frame.h, 200)
        self.assertEqual(frame.wh, (100, 200))
        self.assertEqual(frame.rect, (10, 20, 100, 200))
    
    
    def test_offset(self):
        """Tests whether offset works correctly."""
        
        frame = pero.Frame(10, 20, 100, 200)
        frame.offset(x=10, y=10)
        
        self.assertEqual(frame.x, 20)
        self.assertEqual(frame.y, 30)
        self.assertEqual(frame.width, 100)
        self.assertEqual(frame.height, 200)
    
    
    def test_shrink(self):
        """Tests whether shrinking works correctly."""
        
        frame = pero.Frame(10, 20, 100, 200)
        frame.shrink(1, 2, 3, 4)
        
        self.assertEqual(frame.x1, 14)
        self.assertEqual(frame.y1, 21)
        self.assertEqual(frame.x2, 108)
        self.assertEqual(frame.y2, 217)
        self.assertEqual(frame.width, 94)
        self.assertEqual(frame.height, 196)
    
    
    def test_extend_coordinate(self):
        """Tests whether extension by single coordinate works correctly."""
        
        # test inside x
        frame = pero.Frame(10, 20, 100, 200)
        frame.extend(x=80)
        
        self.assertEqual(frame.x, 10)
        self.assertEqual(frame.y, 20)
        self.assertEqual(frame.width, 100)
        self.assertEqual(frame.height, 200)
        
        # test left x
        frame = pero.Frame(10, 20, 100, 200)
        frame.extend(x=5)
        
        self.assertEqual(frame.x, 5)
        self.assertEqual(frame.y, 20)
        self.assertEqual(frame.width, 105)
        self.assertEqual(frame.height, 200)
        
        # test right x
        frame = pero.Frame(10, 20, 100, 200)
        frame.extend(x=120)
        
        self.assertEqual(frame.x, 10)
        self.assertEqual(frame.y, 20)
        self.assertEqual(frame.width, 110)
        self.assertEqual(frame.height, 200)
        
        # test inside y
        frame = pero.Frame(10, 20, 100, 200)
        frame.extend(y=120)
        
        self.assertEqual(frame.x, 10)
        self.assertEqual(frame.y, 20)
        self.assertEqual(frame.width, 100)
        self.assertEqual(frame.height, 200)
        
        # test top y
        frame = pero.Frame(10, 20, 100, 200)
        frame.extend(y=15)
        
        self.assertEqual(frame.x, 10)
        self.assertEqual(frame.y, 15)
        self.assertEqual(frame.width, 100)
        self.assertEqual(frame.height, 205)
        
        # test bottom y
        frame = pero.Frame(10, 20, 100, 200)
        frame.extend(y=250)
        
        self.assertEqual(frame.x, 10)
        self.assertEqual(frame.y, 20)
        self.assertEqual(frame.width, 100)
        self.assertEqual(frame.height, 230)
    
    
    def test_extend_point(self):
        """Tests whether extension by point works correctly."""
        
        # test inside
        frame = pero.Frame(10, 20, 100, 200)
        frame.extend(x=80, y=120)
        
        self.assertEqual(frame.x, 10)
        self.assertEqual(frame.y, 20)
        self.assertEqual(frame.width, 100)
        self.assertEqual(frame.height, 200)
        
        # test top
        frame = pero.Frame(10, 20, 100, 200)
        frame.extend(x=80, y=15)
        
        self.assertEqual(frame.x, 10)
        self.assertEqual(frame.y, 15)
        self.assertEqual(frame.width, 100)
        self.assertEqual(frame.height, 205)
        
        # test right
        frame = pero.Frame(10, 20, 100, 200)
        frame.extend(x=120, y=120)
        
        self.assertEqual(frame.x, 10)
        self.assertEqual(frame.y, 20)
        self.assertEqual(frame.width, 110)
        self.assertEqual(frame.height, 200)
        
        # test bottom
        frame = pero.Frame(10, 20, 100, 200)
        frame.extend(x=80, y=250)
        
        self.assertEqual(frame.x, 10)
        self.assertEqual(frame.y, 20)
        self.assertEqual(frame.width, 100)
        self.assertEqual(frame.height, 230)
        
        # test left
        frame = pero.Frame(10, 20, 100, 200)
        frame.extend(x=5, y=120)
        
        self.assertEqual(frame.x, 5)
        self.assertEqual(frame.y, 20)
        self.assertEqual(frame.width, 105)
        self.assertEqual(frame.height, 200)
        
        # test top right
        frame = pero.Frame(10, 20, 100, 200)
        frame.extend(x=120, y=15)
        
        self.assertEqual(frame.x, 10)
        self.assertEqual(frame.y, 15)
        self.assertEqual(frame.width, 110)
        self.assertEqual(frame.height, 205)
        
        # test bottom right
        frame = pero.Frame(10, 20, 100, 200)
        frame.extend(x=120, y=250)
        
        self.assertEqual(frame.x, 10)
        self.assertEqual(frame.y, 20)
        self.assertEqual(frame.width, 110)
        self.assertEqual(frame.height, 230)
        
        # test bottom left
        frame = pero.Frame(10, 20, 100, 200)
        frame.extend(x=5, y=250)
        
        self.assertEqual(frame.x, 5)
        self.assertEqual(frame.y, 20)
        self.assertEqual(frame.width, 105)
        self.assertEqual(frame.height, 230)
        
        # test top left
        frame = pero.Frame(10, 20, 100, 200)
        frame.extend(x=5, y=15)
        
        self.assertEqual(frame.x, 5)
        self.assertEqual(frame.y, 15)
        self.assertEqual(frame.width, 105)
        self.assertEqual(frame.height, 205)
    
    
    def test_union(self):
        """Tests whether union works correctly."""
        
        # init frame
        frame = pero.Frame(100, 100, 100, 100)
        
        # no overlap
        test = pero.Frame(0, 0, 10, 10)
        result = frame.union(test)
        
        self.assertEqual(result.x, 0)
        self.assertEqual(result.y, 0)
        self.assertEqual(result.width, 200)
        self.assertEqual(result.height, 200)
        
        test = pero.Frame(200, 150, 100, 100)
        result = frame.union(test)
        
        self.assertEqual(result.x, 100)
        self.assertEqual(result.y, 100)
        self.assertEqual(result.width, 200)
        self.assertEqual(result.height, 150)
        
        test = pero.Frame(150, 200, 100, 100)
        result = frame.union(test)
        
        self.assertEqual(result.x, 100)
        self.assertEqual(result.y, 100)
        self.assertEqual(result.width, 150)
        self.assertEqual(result.height, 200)
        
        # full cover
        test = pero.Frame(0, 0, 200, 200)
        result = frame.union(test)
        
        self.assertEqual(result.x, 0)
        self.assertEqual(result.y, 0)
        self.assertEqual(result.width, 200)
        self.assertEqual(result.height, 200)
        
        # full inside
        test = pero.Frame(125, 125, 50, 50)
        result = frame.union(test)
        
        self.assertEqual(result.x, 100)
        self.assertEqual(result.y, 100)
        self.assertEqual(result.width, 100)
        self.assertEqual(result.height, 100)
        
        # horizontal
        test = pero.Frame(0, 125, 300, 50)
        result = frame.union(test)
        
        self.assertEqual(result.x, 0)
        self.assertEqual(result.y, 100)
        self.assertEqual(result.width, 300)
        self.assertEqual(result.height, 100)
        
        # vertical
        test = pero.Frame(125, 0, 50, 300)
        result = frame.union(test)
        
        self.assertEqual(result.x, 100)
        self.assertEqual(result.y, 0)
        self.assertEqual(result.width, 100)
        self.assertEqual(result.height, 300)
        
        # top-left
        test = pero.Frame(0, 0, 150, 150)
        result = frame.union(test)
        
        self.assertEqual(result.x, 0)
        self.assertEqual(result.y, 0)
        self.assertEqual(result.width, 200)
        self.assertEqual(result.height, 200)
        
        # top-right
        test = pero.Frame(150, 150, 100, 100)
        result = frame.union(test)
        
        self.assertEqual(result.x, 100)
        self.assertEqual(result.y, 100)
        self.assertEqual(result.width, 150)
        self.assertEqual(result.height, 150)
        
        # bottom-left
        test = pero.Frame(0, 150, 150, 150)
        result = frame.union(test)
        
        self.assertEqual(result.x, 0)
        self.assertEqual(result.y, 100)
        self.assertEqual(result.width, 200)
        self.assertEqual(result.height, 200)
        
        # bottom-right
        test = pero.Frame(150, 150, 100, 100)
        result = frame.union(test)
        
        self.assertEqual(result.x, 100)
        self.assertEqual(result.y, 100)
        self.assertEqual(result.width, 150)
        self.assertEqual(result.height, 150)
    
    
    def test_intersection(self):
        """Tests whether intersection works correctly."""
        
        # init frame
        frame = pero.Frame(100, 100, 100, 100)
        
        # no overlap
        test = pero.Frame(0, 0, 10, 10)
        result = frame.intersection(test)
        self.assertTrue(result is None)
        
        test = pero.Frame(200, 150, 100, 100)
        result = frame.intersection(test)
        self.assertTrue(result is None)
        
        test = pero.Frame(150, 200, 100, 100)
        result = frame.intersection(test)
        self.assertTrue(result is None)
        
        # full cover
        test = pero.Frame(0, 0, 200, 200)
        result = frame.intersection(test)
        
        self.assertEqual(result.x, 100)
        self.assertEqual(result.y, 100)
        self.assertEqual(result.width, 100)
        self.assertEqual(result.height, 100)
        
        # full inside
        test = pero.Frame(125, 125, 50, 50)
        result = frame.intersection(test)
        
        self.assertEqual(result.x, 125)
        self.assertEqual(result.y, 125)
        self.assertEqual(result.width, 50)
        self.assertEqual(result.height, 50)
        
        # horizontal
        test = pero.Frame(0, 125, 300, 50)
        result = frame.intersection(test)
        
        self.assertEqual(result.x, 100)
        self.assertEqual(result.y, 125)
        self.assertEqual(result.width, 100)
        self.assertEqual(result.height, 50)
        
        # vertical
        test = pero.Frame(125, 0, 50, 300)
        result = frame.intersection(test)
        
        self.assertEqual(result.x, 125)
        self.assertEqual(result.y, 100)
        self.assertEqual(result.width, 50)
        self.assertEqual(result.height, 100)
        
        # top-left
        test = pero.Frame(0, 0, 150, 150)
        result = frame.intersection(test)
        
        self.assertEqual(result.x, 100)
        self.assertEqual(result.y, 100)
        self.assertEqual(result.width, 50)
        self.assertEqual(result.height, 50)
        
        # top-right
        test = pero.Frame(150, 150, 100, 100)
        result = frame.intersection(test)
        
        self.assertEqual(result.x, 150)
        self.assertEqual(result.y, 150)
        self.assertEqual(result.width, 50)
        self.assertEqual(result.height, 50)
        
        # bottom-left
        test = pero.Frame(0, 150, 150, 150)
        result = frame.intersection(test)
        
        self.assertEqual(result.x, 100)
        self.assertEqual(result.y, 150)
        self.assertEqual(result.width, 50)
        self.assertEqual(result.height, 50)
        
        # bottom-right
        test = pero.Frame(150, 150, 100, 100)
        result = frame.intersection(test)
        
        self.assertEqual(result.x, 150)
        self.assertEqual(result.y, 150)
        self.assertEqual(result.width, 50)
        self.assertEqual(result.height, 50)
    
    
    def test_contains(self):
        """Tests whether contains check works correctly."""
        
        # init frame
        frame = pero.Frame(10, 20, 100, 200)
        
        # test inside x
        self.assertTrue(frame.contains(x=50, y=50))
        
        # test left x
        self.assertFalse(frame.contains(x=5, y=50))
        
        # test right x
        self.assertFalse(frame.contains(x=120, y=50))
        
        # test inside y
        self.assertTrue(frame.contains(x=50, y=50))
        
        # test top y
        self.assertFalse(frame.contains(x=50, y=15))
        
        # test bottom y
        self.assertFalse(frame.contains(x=50, y=250))
    
    
    def test_overlaps(self):
        """Tests whether overlaps check works correctly."""
        
        # init frame
        frame = pero.Frame(100, 100, 100, 100)
        
        # test top-left out
        test = pero.Frame(0, 0, 10, 10)
        self.assertFalse(frame.overlaps(test))
        self.assertFalse(test.overlaps(frame))
        
        # test top-right out
        test = pero.Frame(300, 0, 10, 10)
        self.assertFalse(frame.overlaps(test))
        self.assertFalse(test.overlaps(frame))
        
        # test bottom-right out
        test = pero.Frame(300, 300, 10, 10)
        self.assertFalse(frame.overlaps(test))
        self.assertFalse(test.overlaps(frame))
        
        # test bottom-left out
        test = pero.Frame(0, 300, 10, 10)
        self.assertFalse(frame.overlaps(test))
        self.assertFalse(test.overlaps(frame))
        
        # test top out
        test = pero.Frame(110, 0, 10, 10)
        self.assertFalse(frame.overlaps(test))
        self.assertFalse(test.overlaps(frame))
        
        # test right out
        test = pero.Frame(300, 110, 10, 10)
        self.assertFalse(frame.overlaps(test))
        self.assertFalse(test.overlaps(frame))
        
        # test bottom out
        test = pero.Frame(110, 300, 10, 10)
        self.assertFalse(frame.overlaps(test))
        self.assertFalse(test.overlaps(frame))
        
        # test left out
        test = pero.Frame(0, 110, 10, 10)
        self.assertFalse(frame.overlaps(test))
        self.assertFalse(test.overlaps(frame))
        
        # test inside
        test = pero.Frame(110, 110, 10, 10)
        self.assertTrue(frame.overlaps(test))
        self.assertTrue(test.overlaps(frame))
        
        # test top-left in
        test = pero.Frame(0, 0, 110, 110)
        self.assertTrue(frame.overlaps(test))
        self.assertTrue(test.overlaps(frame))
        
        # test top-right in
        test = pero.Frame(195, 0, 110, 110)
        self.assertTrue(frame.overlaps(test))
        self.assertTrue(test.overlaps(frame))
        
        # test bottom-right in
        test = pero.Frame(195, 195, 110, 110)
        self.assertTrue(frame.overlaps(test))
        self.assertTrue(test.overlaps(frame))
        
        # test bottom-left in
        test = pero.Frame(0, 195, 110, 110)
        self.assertTrue(frame.overlaps(test))
        self.assertTrue(test.overlaps(frame))


# run test case
if __name__ == "__main__":
    unittest.main(verbosity=2)
