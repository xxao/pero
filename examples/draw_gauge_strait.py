#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for strait gauge drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # init coords
        padding = 30
        spacing = 10
        bars = 8
        width, height = canvas.viewport.wh
        
        # init gauge
        gauge = pero.StraitGauge(
            bgr_line_color = "#00a7",
            bgr_fill_color = "#00a3",
            for_line_color = "#00fb",
            for_fill_color = "#00f6")
        
        # draw horizontal bars
        gauge.orientation = pero.HORIZONTAL
        gauge.length = 0.5 * (width - 3*padding)
        gauge.thickness = (height - 2*padding - (bars-1)*spacing) / bars
        gauge.radius = 0.5 * gauge.thickness
        
        x = padding
        y = padding
        
        gauge.draw(canvas, x=x, y=y, start=0, end=1)
        y += gauge.thickness + spacing
        gauge.draw(canvas, x=x, y=y, start=0.25, end=0.5)
        y += gauge.thickness + spacing
        gauge.draw(canvas, x=x, y=y, start=0.25, end=0.5, reverse=True)
        y += gauge.thickness + spacing
        gauge.draw(canvas, x=x, y=y, start=-0.25, end=0.5)
        y += gauge.thickness + spacing
        gauge.draw(canvas, x=x, y=y, start=0.5, end=1.75)
        y += gauge.thickness + spacing
        gauge.draw(canvas, x=x, y=y, start=0.5, end=0.5)
        y += gauge.thickness + spacing
        gauge.draw(canvas, x=x, y=y, start=-0.5, end=0)
        y += gauge.thickness + spacing
        gauge.draw(canvas, x=x, y=y, start=1, end=1.1)
        
        # draw vertical bars
        gauge.orientation = pero.VERTICAL
        gauge.length = height - 2*padding
        gauge.thickness = ((0.5 * (width - 3*padding)) - (bars-1)*spacing) / bars
        gauge.radius = 0.5 * gauge.thickness
        
        x = 0.5 * (width + padding)
        y = padding
        
        gauge.draw(canvas, x=x, y=y, start=0, end=1)
        x += gauge.thickness + spacing
        gauge.draw(canvas, x=x, y=y, start=0.25, end=0.5)
        x += gauge.thickness + spacing
        gauge.draw(canvas, x=x, y=y, start=0.25, end=0.5, reverse=True)
        x += gauge.thickness + spacing
        gauge.draw(canvas, x=x, y=y, start=-0.25, end=0.5)
        x += gauge.thickness + spacing
        gauge.draw(canvas, x=x, y=y, start=0.5, end=1.75)
        x += gauge.thickness + spacing
        gauge.draw(canvas, x=x, y=y, start=0.5, end=0.5)
        x += gauge.thickness + spacing
        gauge.draw(canvas, x=x, y=y, start=-0.5, end=0)
        x += gauge.thickness + spacing
        gauge.draw(canvas, x=x, y=y, start=1, end=1.1)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Strait Gauge", 450, 250)
