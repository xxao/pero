#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for angled text drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # init glyphs
        origin = pero.Plus(
            line_width = 1,
            line_color = pero.colors.Red,
            size = 10)
        
        label = pero.Text(
            font_size = 14,
            text_align = pero.CENTER,
            text_base = pero.MIDDLE,
            text_bgr_color = "lightgrey",
            angle_units = pero.DEG)
        
        # init coords
        x = 70
        y = 70
        
        # test angles
        for angle in range(-360, 360, 45):
            
            if x+80 > 400:
                x = 70
                y += 100
            
            title = "ANGLE%d" % angle
            label.draw(canvas, x=x, y=y, text=title, angle=angle)
            origin.draw(canvas, x=x, y=y)
            
            x += 80


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Text Angle", 400, 450)
