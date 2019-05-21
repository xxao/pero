#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import numpy
import pero


class DrawTest(pero.Graphics):
    """Test case for manually assembled plot drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # init range
        x_range = (-2*numpy.pi, 2*numpy.pi)
        y_range = (-1.5, 1.5)
        
        # make series
        x_data = numpy.linspace(x_range[0], x_range[1], 50)
        sin_data = numpy.sin(x_data)
        cos_data = numpy.cos(x_data)
        
        # init x-axis
        x_scale = pero.LinScale(in_range=x_range)
        x_ticker = pero.LinTicker(start=x_range[0], end=x_range[1], major_splits=[numpy.pi], minor_splits=[.5*numpy.pi], minor_count=3)
        x_ticker.formatter = pero.FuncFormatter(func=lambda d: "%d pi" % (d/numpy.pi))
        x_ticks_maj = x_ticker.major_ticks()
        x_ticks_min = x_ticker.minor_ticks()
        x_labels = x_ticker.labels()
        x_axis = pero.StraitAxis(title="angle", labels=x_labels, title_offset=25, relative=False)
        x_grid = pero.ParallelGrid(line_color="lightgray", orientation=pero.VERTICAL)
        
        # init y-axis
        y_scale = pero.LinScale(in_range=y_range)
        y_ticker = pero.LinTicker(start=y_range[0], end=y_range[1])
        y_ticks_maj = y_ticker.major_ticks()
        y_ticks_min = y_ticker.minor_ticks()
        y_labels = y_ticker.labels()
        y_axis = pero.StraitAxis(title="fn(x)", labels=y_labels, title_offset=30, relative=False, position=pero.LEFT)
        y_grid = pero.ParallelGrid(line_color="lightgray")
        
        # init series glyph
        series_glyph = pero.Circle()
        series_glyph.x = lambda d: x_scale.scale(d[0])
        series_glyph.y = lambda d: y_scale.scale(d[1])
        
        # calc coordinates
        padding = 60
        width, height = canvas.viewport.wh
        h_length = width - 2*padding
        v_length = height - 2*padding
        
        # set scale range
        x_scale.out_range = (padding, width-padding)
        y_scale.out_range = (height-padding, padding)
        
        # scale ticks
        x_ticks_maj = x_scale.scale(x_ticks_maj)
        x_ticks_min = x_scale.scale(x_ticks_min)
        y_ticks_maj = y_scale.scale(y_ticks_maj)
        y_ticks_min = y_scale.scale(y_ticks_min)
        
        # draw grids
        x_grid.draw(canvas, y=padding, length=v_length, ticks=x_ticks_min, line_alpha=60)
        y_grid.draw(canvas, x=padding, length=h_length, ticks=y_ticks_min, line_alpha=60)
        
        x_grid.draw(canvas, y=padding, length=v_length, ticks=x_ticks_maj)
        y_grid.draw(canvas, x=padding, length=h_length, ticks=y_ticks_maj)
        
        # draw axes
        x_axis.draw(canvas, x=padding, y=height-padding, length=h_length, major_ticks=x_ticks_maj, minor_ticks=x_ticks_min)
        y_axis.draw(canvas, x=padding, y=padding, length=v_length, major_ticks=y_ticks_maj, minor_ticks=y_ticks_min)
        
        # draw series
        canvas.clip(pero.Path().rect(padding, padding, h_length, v_length))
        
        for i, y_data in enumerate((sin_data, cos_data)):
            
            series_glyph.line_color = pero.colors.Pero[i]
            series_glyph.fill_color = pero.colors.Pero[i].opaque(.75)
            
            canvas.group()
            for j in range(len(x_data)):
                series_glyph.draw(canvas, source=(x_data[j], y_data[j]))
            canvas.ungroup()
        
        canvas.unclip()


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Plot", 600, 400)
