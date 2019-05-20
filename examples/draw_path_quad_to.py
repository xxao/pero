#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for path quadratic curve drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # make path
        path = pero.Path.from_svg("M70,250 Q20,110  208,63")
        
        # draw points
        canvas.line_color = "red"
        canvas.draw_line(x1=70, y1=250, x2=20, y2=110)
        canvas.draw_line(x1=20, y1=110, x2=208, y2=63)
        canvas.draw_circle(x=70, y=250, radius=5)
        canvas.draw_circle(x=20, y=110, radius=5)
        canvas.draw_circle(x=208, y=63, radius=5)
        
        # draw path
        pather = pero.Pather(path=path)
        pather.draw(canvas)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Path QuadTo", 250, 300)
