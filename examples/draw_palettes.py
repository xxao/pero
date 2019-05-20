#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for named palettes."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # set properties
        rect_width = 17
        rect_height = 17
        
        # init glyphs
        label = pero.Text(text_base=pero.MIDDLE)
        
        rect = pero.Rect(
            line_width = 1,
            line_color = pero.colors.White,
            width = rect_width,
            height = rect_height)
        
        # init coords
        x = 50
        y = 50
        
        # draw palettes
        for palette in sorted(pero.PALETTES, key=lambda d:d.name):
            
            if x + rect.width * len(palette) > 900:
                x = 50
                y += round(2.5*rect.height)
            
            title = "%s (%d)" % (palette.name, len(palette))
            label.draw(canvas, x=x, y=y, text=title)
            
            for color in palette.colors:
                rect.draw(canvas, x=x, y=y+10, fill_color=color)
                x += rect.width - rect.line_width
            
            x += 50


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Palettes", 900, 550)
