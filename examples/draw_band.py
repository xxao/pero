#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import pero


class DrawTest(pero.Graphics):
    """Test case for band drawing."""
    
    
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
        y1_data = numpy.sin(x_data) * .5 + .5
        y2_data = y1_data - 1.
        data = numpy.stack((x_data, y1_data, y2_data), axis=1)
        
        # init scales
        x_scale = pero.LinScale()
        x_scale.in_range = (x_data[0], x_data[-1])
        x_scale.out_range = (padding, width-padding)
        
        y_scale = pero.LinScale()
        y_scale.in_range = (-1, 1)
        y_scale.out_range = (y+size-padding, y)
        
        # init glyph (with dynamic fill)
        glyph = pero.Band(
            line_color = pero.colors.Blue,
            fill_color = pero.colors.Blue.lighter(0.7),
            data = data,
            marker_size = 8,
            marker_line_color = pero.colors.White,
            marker_fill_color = lambda d: "b" if d[0] >= 0 else "r")
        
        # draw lines
        glyph.draw(canvas,
            x = x_scale.scale(x_data),
            y1 = y_scale.scale(y1_data),
            y2 = y_scale.scale(y2_data),
            show_line = True,
            show_points = False,
            show_area = False)
        
        y += size
        y_scale.out_range = (y+size-padding, y)
        
        # draw points
        glyph.draw(canvas,
            x = x_scale.scale(x_data),
            y1 = y_scale.scale(y1_data),
            y2 = y_scale.scale(y2_data),
            show_line = False,
            show_points = True,
            show_area = False)
        
        y += size
        y_scale.out_range = (y+size-padding, y)
        
        # draw area
        glyph.draw(canvas,
            x = x_scale.scale(x_data),
            y1 = y_scale.scale(y1_data),
            y2 = y_scale.scale(y2_data),
            show_line = False,
            show_points = False,
            show_area = True)
        
        y += size
        y_scale.out_range = (y+size-padding, y)
        
        # draw line and area
        glyph.draw(canvas,
            x = x_scale.scale(x_data),
            y1 = y_scale.scale(y1_data),
            y2 = y_scale.scale(y2_data),
            show_line = True,
            show_points = False,
            show_area = True)
        
        y += size
        y_scale.out_range = (y+size-padding, y)
        
        # draw all
        glyph.draw(canvas,
            x = x_scale.scale(x_data),
            y1 = y_scale.scale(y1_data),
            y2 = y_scale.scale(y2_data),
            show_line = True,
            show_points = pero.UNDEF,
            show_area = True)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Band", 400, 400)
