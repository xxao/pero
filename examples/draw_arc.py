#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math
import pero


class DrawTest(pero.Graphics):
    """Test case for arc drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        x = 70
        y = 70
        radius = 40
        
        canvas.line_color = pero.colors.Blue
        canvas.draw_arc(x, y, radius, math.radians(0), math.radians(90), True)
        
        x += 100
        canvas.line_color = pero.colors.Blue
        canvas.draw_arc(x, y, radius, math.radians(0), math.radians(90), False)
        
        x += 100
        canvas.line_color = pero.colors.Blue
        canvas.draw_arc(x, y, radius, math.radians(90), math.radians(0), True)
        
        x += 100
        canvas.line_color = pero.colors.Blue
        canvas.draw_arc(x, y, radius, math.radians(90), math.radians(0), False)
        
        x = 70
        y += 100
        canvas.line_color = pero.colors.Blue
        canvas.draw_arc(x, y, radius, math.radians(-30), math.radians(200), True)
        
        x += 100
        canvas.line_color = pero.colors.Blue
        canvas.draw_arc(x, y, radius, math.radians(-30), math.radians(200), False)
        
        x += 100
        canvas.line_color = pero.colors.Blue
        canvas.draw_arc(x, y, radius, math.radians(200), math.radians(-30), True)
        
        x += 100
        canvas.line_color = pero.colors.Blue
        canvas.draw_arc(x, y, radius, math.radians(200), math.radians(-30), False)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Arc", 450, 250)
