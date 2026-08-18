#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import unittest
import pero


class TestCase(unittest.TestCase):
    """Test case for layout calculations."""
    
    
    def test_asymmetric_padding_center(self):
        """Tests centering within asymmetric padding."""
        
        layout = pero.Layout(width=100, height=100)
        layout.add(
            pero.Graphics(), 0, 0,
            width=20,
            height=20,
            padding=(20, 0, 0, 20),
            h_expand=False,
            v_expand=False)
        
        layout.arrange()
        
        self.assertEqual(layout.cells[0].content.rect, (50, 50, 20, 20))
    
    
    def test_asymmetric_padding_expand(self):
        """Tests expansion within asymmetric padding."""
        
        layout = pero.Layout(width=100, height=100)
        layout.add(
            pero.Graphics(), 0, 0,
            padding=(20, 0, 0, 20))
        
        layout.arrange()
        
        self.assertEqual(layout.cells[0].content.rect, (20, 20, 80, 80))
    
    
    def test_minimum_includes_padding(self):
        """Tests whether content minimum includes cell padding."""
        
        layout = pero.Layout(width=0, height=0)
        layout.add(
            pero.Graphics(), 0, 0,
            width=50,
            height=30,
            padding=10)
        
        layout.arrange()
        
        self.assertEqual(layout.cells[0].frame.rect, (0, 0, 70, 50))
        self.assertEqual(layout.cells[0].content.rect, (10, 10, 50, 30))
    
    
    def test_minimum_across_span(self):
        """Tests whether content minimum is enforced across a span."""
        
        layout = pero.Layout(width=30, height=20, spacing=10)
        layout.add(
            pero.Graphics(), 0, 0,
            col_span=2,
            width=100,
            padding=(0, 10, 0, 10))
        
        layout.arrange()
        
        cell = layout.cells[0]
        self.assertEqual(cell.frame.width, 120)
        self.assertEqual(cell.content.width, 100)
    
    
    def test_minimum_with_mixed_tracks(self):
        """Tests a spanning minimum across fixed and relative tracks."""
        
        layout = pero.Layout(width=50, height=20)
        layout.add_col(20, relative=False)
        layout.add_col(1, relative=True)
        layout.add(
            pero.Graphics(), 0, 0,
            col_span=2,
            width=100)
        
        layout.arrange()
        
        self.assertEqual(layout.cells[0].frame.width, 100)
        self.assertEqual(layout.cols[0].width, 20)


if __name__ == "__main__":
    unittest.main(verbosity=2)
