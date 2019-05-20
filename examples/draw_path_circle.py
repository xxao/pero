#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for Bezier circle drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # init coords
        width, height = canvas.viewport.wh
        x = 0.5*width
        y = 0.5*height
        r = 0.5*min(width, height) - 2*20
        
        # make circle path
        path = pero.Path()
        path.circle(x, y, r)
        
        # draw standard circle
        canvas.line_color = pero.colors.Grey
        canvas.draw_circle(x, y, r)
        
        # draw path circle
        glyph = pero.Pather(path=path)
        glyph.draw(canvas, fill_color=None, line_color=pero.colors.Red)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Bezier Circle", 300, 300)
