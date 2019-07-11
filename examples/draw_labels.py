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
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # init scales
        x_scale = pero.LinScale(in_range=(0, 1), out_range=(0, canvas.viewport.w))
        y_scale = pero.LinScale(in_range=(0, 1), out_range=(0, canvas.viewport.h))
        z_scale = pero.GradientScale(in_range=(0, 1), out_range=pero.colors.YlOrBr)
        
        # init label glyph
        label = pero.TextLabel(
            x = lambda d: x_scale.scale(d[0]),
            y = lambda d: y_scale.scale(d[1]),
            z_index = lambda d: d[2],
            text = lambda d: "(%.0f - %.0f)" % (x_scale.scale(d[0]), y_scale.scale(d[1])),
            font_size = 12)
        
        # init labels
        labels = []
        for point in self._values:
            labels.append(label.clone(source=point))
        
        # init container
        container = pero.Labels(
            items = labels,
            overlap = False,
            spacing = 4,
            clip = canvas.viewport)
        
        # init marker
        marker = pero.Circle(
            size = 8,
            line_width = 0)
        
        # draw markers
        for x, y, z in self._values:
            marker.draw(canvas,
                x = x_scale.scale(x),
                y = y_scale.scale(y),
                fill_color = z_scale.scale(z))
        
        # draw labels
        container.draw(canvas)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'wx', "Labels", 600, 600)
