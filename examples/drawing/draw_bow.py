#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for bow drawing."""
    
    
    def draw(self, canvas, *args, **kwargs):
        """Draws the test."""
        
        # clear canvas
        canvas.fill(pero.colors.White)
        canvas.line_width = 4
        
        radius = 50
        
        canvas.view(2*radius, 1.5*radius)
        canvas.line_color = pero.colors.LightGrey
        canvas.draw_circle(-25, 0, radius)
        canvas.draw_circle(+25, 0, radius)
        
        canvas.line_color = pero.colors.Blue
        canvas.draw_bow(0, -43, 0, 43, radius, large=True, clockwise=True)
        
        canvas.view(6*radius, 1.5*radius)
        canvas.line_color = pero.colors.LightGrey
        canvas.draw_circle(-25, 0, radius)
        canvas.draw_circle(+25, 0, radius)
        
        canvas.line_color = pero.colors.Blue
        canvas.draw_bow(0, -43, 0, 43, radius, large=False, clockwise=True)
        
        canvas.view(2*radius, 4.5*radius)
        canvas.line_color = pero.colors.LightGrey
        canvas.draw_circle(-25, 0, radius)
        canvas.draw_circle(+25, 0, radius)
        
        canvas.line_color = pero.colors.Blue
        canvas.draw_bow(0, -43, 0, 43, radius, large=True, clockwise=False)
        
        canvas.view(6*radius, 4.5*radius)
        canvas.line_color = pero.colors.LightGrey
        canvas.draw_circle(-25, 0, radius)
        canvas.draw_circle(+25, 0, radius)

        canvas.line_color = pero.colors.Blue
        canvas.draw_bow(0, -43, 0, 43, radius, large=False, clockwise=False)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Bow", 400, 300)
