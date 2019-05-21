#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for color bar drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # init coords
        padding = 30
        spacing = 20
        bars = 2
        width, height = canvas.viewport.wh
        
        # init color bar
        bar = pero.ColorBar(
            steps = 128,
            gradient = pero.colors.YlOrBr)
        
        # draw horizontal bars
        bar.orientation = pero.HORIZONTAL
        bar.length = 0.5 * (width - 3*padding)
        bar.thickness = (height - 2*padding - (bars-1)*spacing) / bars
        
        x = padding
        y = padding
        
        bar.draw(canvas, x=x, y=y)
        y += bar.thickness + spacing
        bar.draw(canvas, x=x, y=y, reverse=True)
        
        # draw vertical bars
        bar.orientation = pero.VERTICAL
        bar.length = height - 2*padding
        bar.thickness = ((0.5 * (width - 3*padding)) - (bars-1)*spacing) / bars
        
        x = 0.5 * (width + padding)
        y = padding
        
        bar.draw(canvas, x=x, y=y)
        x += bar.thickness + spacing
        bar.draw(canvas, x=x, y=y, reverse=True)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Color Bar", 450, 250)
