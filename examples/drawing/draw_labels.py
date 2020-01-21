#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import pero


class DrawTest(pero.Graphics):
    """Test case for labels drawing."""
    
    
    def __init__(self):
        """Initializes a new instance of DrawTest."""
        
        super(DrawTest, self).__init__()
        
        self._values = numpy.random.rand(50, 3)
    
    
    def draw(self, canvas, *args, **kwargs):
        """Draws the test."""
        
        # clear canvas
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # init scales
        x_scale = pero.LinScale(in_range=(0, 1), out_range=(0, canvas.viewport.w))
        y_scale = pero.LinScale(in_range=(0, 1), out_range=(0, canvas.viewport.h))
        z_scale = pero.GradientScale(in_range=(0, 1), out_range=pero.colors.YlOrBr)
        
        # init marker glyph
        marker = pero.Circle(
            x = lambda d: x_scale.scale(d[0]),
            y = lambda d: y_scale.scale(d[1]),
            fill_color = lambda d: z_scale.scale(d[2]),
            size = 8,
            line_width = 0)
        
        # init label glyph
        label = pero.TextLabel(
            x = lambda d: x_scale.scale(d[0]),
            y = lambda d: y_scale.scale(d[1]),
            z_index = lambda d: d[2],
            y_offset = -5,
            text = lambda d: "(%.0f - %.0f)" % (x_scale.scale(d[0]), y_scale.scale(d[1])),
            font_size = 12)
        
        # init container glyph
        container = pero.LabelBox(
            overlap = False,
            spacing = 4,
            padding = 5,
            clip = canvas.viewport)
        
        # draw markers
        marker.draw_many(canvas, self._values)
        
        # create labels
        labels = [label.clone(source=val) for val in self._values]
        
        # draw labels
        container.draw(canvas, items=labels)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Labels", 600, 600)
