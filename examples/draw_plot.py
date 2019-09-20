#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import pero


class DrawTest(pero.Graphics):
    """Test case for manually assembled plot drawing."""
    
    
    def __init__(self):
        """Initializes plot."""
        
        super(DrawTest, self).__init__()
        
        # init data range
        x_range = (-2 * numpy.pi, 2 * numpy.pi)
        y_range = (-1.5, 1.5)
        
        # make series
        self.x_data = numpy.linspace(x_range[0], x_range[1], 50)
        self.sin_data = numpy.sin(self.x_data)
        self.cos_data = numpy.cos(self.x_data)
        
        # init scales
        self.x_scale = pero.LinScale(in_range=x_range)
        self.y_scale = pero.LinScale(in_range=y_range)
        
        # init x-axis
        self.x_ticker = pero.LinTicker(
            start = x_range[0],
            end = x_range[1],
            major_splits = [numpy.pi],
            minor_splits = [.5*numpy.pi],
            minor_count = 3,
            formatter = pero.FuncFormatter(func=lambda d: "%d pi" % (d/numpy.pi)))
        
        self.x_axis = pero.StraitAxis(
            title = "angle",
            labels = self.x_ticker.labels(),
            title_offset = 25,
            relative = False,
            position = pero.BOTTOM)
        
        self.x_grid = pero.ParallelGrid(
            line_color = "lightgrey",
            orientation = pero.VERTICAL)
        
        # init y-axis
        self.y_ticker = pero.LinTicker(
            start = y_range[0],
            end = y_range[1])
        
        self.y_axis = pero.StraitAxis(
            title = "fn(x)",
            labels = self.y_ticker.labels(),
            title_offset = 30,
            relative = False,
            position = pero.LEFT)
        
        self.y_grid = pero.ParallelGrid(
            line_color = "lightgrey",
            orientation = pero.HORIZONTAL)
        
        # init series marker
        self.marker = pero.Circle(
            x = lambda d: self.x_scale.scale(d[0]),
            y = lambda d: self.y_scale.scale(d[1]))
        
        # init labels glyph
        self.label = pero.TextLabel(
            x = lambda d: self.x_scale.scale(d[0]),
            y = lambda d: self.y_scale.scale(d[1]),
            z_index = lambda d: abs(d[1]),
            x_offset = 10,
            y_offset = lambda d: -10*d[1],
            text = lambda d: "%.2f" % d[1],
            text_align = pero.LEFT,
            text_base = pero.MIDDLE,
            text_color = "grey")
        
        self.labels = pero.Labels(
            overlap = False,
            spacing = 4,
            padding = 10)
        
        # init legend
        self.legend = pero.Legends(
            orientation = pero.HORIZONTAL,
            anchor = pero.N)
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # calc coordinates
        padding = 50
        width, height = canvas.viewport.wh
        h_length = width - 2*padding
        v_length = height - 2*padding
        frame = pero.Frame(padding, padding, h_length, v_length)
        
        # set scale range
        self.x_scale.out_range = (padding, width-padding)
        self.y_scale.out_range = (height-padding, padding)
        
        # scale ticks
        x_ticks_maj = self.x_scale.scale(self.x_ticker.major_ticks())
        x_ticks_min = self.x_scale.scale(self.x_ticker.minor_ticks())
        y_ticks_maj = self.y_scale.scale(self.y_ticker.major_ticks())
        y_ticks_min = self.y_scale.scale(self.y_ticker.minor_ticks())
        
        # draw grids
        self.x_grid.draw(canvas, y=padding, length=v_length, ticks=x_ticks_min, line_alpha=60)
        self.y_grid.draw(canvas, x=padding, length=h_length, ticks=y_ticks_min, line_alpha=60)
        self.x_grid.draw(canvas, y=padding, length=v_length, ticks=x_ticks_maj)
        self.y_grid.draw(canvas, x=padding, length=h_length, ticks=y_ticks_maj)
        
        # draw axes
        self.x_axis.draw(canvas, x=padding, y=height-padding, length=h_length, major_ticks=x_ticks_maj, minor_ticks=x_ticks_min)
        self.y_axis.draw(canvas, x=padding, y=padding, length=v_length, major_ticks=y_ticks_maj, minor_ticks=y_ticks_min)
        
        # apply clipping
        with canvas.clip(pero.Path().rect(*frame.rect)):
            
            # draw series
            for i, y_data in enumerate((self.sin_data, self.cos_data)):
                with canvas.group():
                    self.marker.line_color = pero.colors.Pero[i]
                    self.marker.fill_color = pero.colors.Pero[i].opaque(.75)
                    self.marker.draw_many(canvas, zip(self.x_data, y_data))
            
            # draw labels
            labels = []
            for y_data in (self.sin_data, self.cos_data):
                labels += [self.label.clone(source=val) for val in zip(self.x_data, y_data)]
            
            self.labels.draw(canvas, items=labels, clip=frame)
        
        # draw legend
        legends = []
        for i, text in enumerate(('sin(x)', 'cos(x)')):
            
            legend = pero.MarkerLegend(
                text = text,
                marker = pero.MARKER.CIRCLE,
                marker_line_color=pero.colors.Pero[i],
                marker_fill_color=pero.colors.Pero[i].opaque(.75))
            
            legends.append(legend)
        
        self.legend.draw(canvas, items=legends, x=.5*width, y=15)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Plot", 600, 400)
