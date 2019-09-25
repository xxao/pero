#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for text box drawing."""
    
    
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
            anchor = pero.UNDEF,
            line_color = pero.colors.Grey,
            fill_color = pero.colors.LightGrey,
            text = "Lorem ipsum\ndolor sit amet,\nconsectetur adipiscing\nelit.")
        
        origin = pero.Plus(
            line_width = 1,
            line_color = pero.colors.Red,
            size = 10)
        
        # init values
        aligns = (
            pero.LEFT,
            pero.CENTER,
            pero.RIGHT)
        
        baselines = (
            pero.TOP,
            pero.MIDDLE,
            pero.BOTTOM)
        
        # init coords
        margin = 25
        w, h = canvas.viewport.wh
        x_step = (w - 2*margin) / 2
        y_step = (h - 2*margin) / 2
        y = margin
        
        # draw tests
        for baseline in baselines:
            
            x = margin
            for align in aligns:
                
                textbox.draw(canvas, x=x, y=y, text_align=align, text_base=baseline)
                origin.draw(canvas, x=x, y=y)
                
                x += x_step
            y += y_step


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Text Box", 500, 300)
