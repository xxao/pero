#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for text box with anchor drawing."""
    
    
    def draw(self, canvas, *args, **kwargs):
        """Draws the test."""
        
        # clear canvas
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # init glyphs
        textbox = pero.Textbox(
            radius = 5,
            angle = 10,
            angle_units = pero.DEG,
            text_align = pero.RIGHT,
            line_color = pero.colors.Grey,
            fill_color = pero.colors.LightGrey,
            text = "Lorem ipsum\ndolor sit amet,\nconsectetur adipiscing\nelit.")
        
        origin = pero.Plus(
            line_width = 1,
            line_color = pero.colors.Red,
            size = 10)
        
        # init values
        anchors = (
            pero.NW,
            pero.N,
            pero.NE,
            pero.W,
            pero.C,
            pero.E,
            pero.SW,
            pero.S,
            pero.SE)
        
        # init coords
        margin = 25
        w, h = canvas.viewport.wh
        x_step = (w - 2*margin) / 2
        y_step = (h - 2*margin) / 2
        x = 0
        y = margin - y_step
        
        # draw tests
        for i, anchor in enumerate(anchors):
            
            if i % 3 == 0:
                x = margin
                y += y_step
            
            textbox.draw(canvas, x=x, y=y, anchor=anchor)
            origin.draw(canvas, x=x, y=y)
            
            x += x_step


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Text Box with Anchor", 500, 300)
