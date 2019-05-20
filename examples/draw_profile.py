#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import pero


class DrawTest(pero.Graphics):
    """Test case for profile drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # calc coordinates
        width, height = canvas.viewport.wh
        padding = 30
        size = (height - padding) / 5
        y = padding
        
        # init data
        x_data = numpy.linspace(-numpy.pi, numpy.pi, 20)
        y_data = numpy.sin(x_data)
        data = numpy.stack((x_data, y_data), axis=1)
        
        # init scales
        x_scale = pero.LinScale()
        x_scale.in_range = (x_data[0], x_data[-1])
        x_scale.out_range = (padding, width-padding)
        
        y_scale = pero.LinScale()
        y_scale.in_range = (-1, 1)
        y_scale.out_range = (y+size-padding, y)
        
        # init glyph (with dynamic fill)
        glyph = pero.Profile(
            data = data,
            line_color = pero.colors.Blue,
            fill_color = pero.colors.Blue.lighter(0.7),
            marker_size = 8,
            marker_line_color = pero.colors.White,
            marker_fill_color = lambda d: "b" if d[0] >= 0 else "r")
        
        # draw line
        glyph.draw(canvas,
            x = x_scale.scale(x_data),
            y = y_scale.scale(y_data),
            show_line = True,
            show_points = False)
        
        y += size
        y_scale.out_range = (y+size-padding, y)
        
        # draw points
        glyph.draw(canvas,
            x = x_scale.scale(x_data),
            y = y_scale.scale(y_data),
            show_line = False)
        
        y += size
        y_scale.out_range = (y+size-padding, y)
        
        # draw line with auto points
        glyph.draw(canvas,
            x = x_scale.scale(x_data),
            y = y_scale.scale(y_data),
            show_line = True,
            show_points = pero.UNDEF)
        
        y += size
        y_scale.out_range = (y+size-padding, y)
        
        # draw area
        glyph.draw(canvas,
            x = x_scale.scale(x_data),
            y = y_scale.scale(y_data),
            show_area = True)
        
        y += size
        y_scale.out_range = (y+size-padding, y)
        
        # draw area to base
        glyph.draw(canvas,
            x = x_scale.scale(x_data),
            y = y_scale.scale(y_data),
            base = y_scale.scale(-1.5),
            show_area = True)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Profile", 400, 400)
