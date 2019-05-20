#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for named colors."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # set properties
        padding = 50
        spacing = 7
        size = 20
        column = 160
        height = canvas.height
        
        # init glyphs
        label = pero.Text(
            text_align = pero.LEFT,
            text_base = pero.MIDDLE)
        
        glyph = pero.Circle(
            line_color = pero.colors.Grey,
            line_width = 1,
            size = size)
        
        # init coords
        x = padding
        y = padding
        
        # draw colors
        for color in sorted(pero.COLORS, key=lambda d:d.name):
            
            glyph.draw(canvas, x=x, y=y, fill_color=color)
            label.draw(canvas, x=x+size, y=y, text=color.name)
            
            y += size + spacing
            if y > height - 0.5*size - padding:
                y = padding
                x += column + size


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Colors", 1090, 820)
