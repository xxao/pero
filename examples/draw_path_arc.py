#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for Bezier arc drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # init path
        start_angle = pero.rads(30)
        end_angle = pero.rads(100)
        clockwise = True
        
        # init coords
        width, height = canvas.viewport.wh
        x = 0.5*width
        y = 0.5*height
        r = 0.5*min(width, height) - 2*20
        
        # make arc path
        path = pero.Path()
        path.arc(x, y, r, start_angle, end_angle, clockwise)
        
        # draw angles rays
        ray = pero.Ray(x=x, y=y, length=r+10)
        ray.draw(canvas, angle=start_angle, line_color=pero.colors.Red)
        ray.draw(canvas, angle=end_angle, line_color=pero.colors.Green)
        
        # draw standard arc
        canvas(line_color=pero.colors.Grey, fill_color=None)
        canvas.draw_circle(x, y, r)
        # canvas.draw_path(pero.Path().circle(x, y, r))
        
        # draw path arc
        glyph = pero.Pather(path=path)
        glyph.draw(canvas, fill_color=None, line_color=pero.colors.Red)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Bezier Arc", 300, 300)
