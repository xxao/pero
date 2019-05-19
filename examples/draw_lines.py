#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for profile drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.Color.White
        canvas.fill()
        
        # calc coordinates
        padding = 30
        margin = 60
        width, height = canvas.viewport.wh
        x1 = padding
        x2 = width - padding
        y = padding
        
        # init label
        label = pero.Text()
        
        # init glyph
        glyph = pero.Line(
            line_color = pero.Color.Black,
            line_width = 5,
            line_cap = pero.BUTT,
            line_join = pero.MITER)
        
        # draw solid line
        label.draw(canvas, x=x1, y=y+10, text="Solid")
        glyph.draw(canvas, x1=x1, y1=y, x2=x2, y2=y, line_style=pero.SOLID)
        
        # draw dashed line
        y += margin
        label.draw(canvas, x=x1, y=y+10, text="Dashed")
        glyph.draw(canvas, x1=x1, y1=y, x2=x2, y2=y, line_style=pero.DASHED)
        
        # draw dashed line
        y += margin
        label.draw(canvas, x=x1, y=y+10, text="Dotted")
        glyph.draw(canvas, x1=x1, y1=y, x2=x2, y2=y, line_style=pero.DOTTED)
        
        # draw dash-dotted line
        y += margin
        label.draw(canvas, x=x1, y=y+10, text="Dash-Dotted")
        glyph.draw(canvas, x1=x1, y1=y, x2=x2, y2=y, line_style=pero.DASHDOTTED)
        
        # draw custom line
        y += margin
        label.draw(canvas, x=x1, y=y+10, text="Custom")
        glyph.draw(canvas, x1=x1, y1=y, x2=x2, y2=y, line_style=pero.CUSTOM, line_dash=[5,7,1,2,1,7])


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Line Styles", 400, 330)
