#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for text box drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # init glyphs
        textbox = pero.Textbox(
            font_name = "Arial",
            font_size = 11,
            line_color = "grey",
            fill_color = "lightgrey",
            radius = 5,
            angle = 15,
            angle_units = pero.DEG,
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
        
        # draw tests
        y = 25
        for baseline in baselines:
            
            x = 25
            for align in aligns:
                
                textbox.draw(canvas, x=x, y=y, text_align=align, text_base=baseline)
                origin.draw(canvas, x=x, y=y)
                
                x += 250
            y += 150


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Text Box", 550, 350)
