#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for legend drawing."""
    
    
    def draw(self, canvas, *args, **kwargs):
        """Draws the test."""
        
        # clear canvas
        canvas.fill(pero.colors.White)
        
        # init coords
        padding = 20
        width, height = canvas.viewport.wh
        
        # init legend items
        legend1 = pero.MarkerLegend(
            text = "First legend",
            marker = "o",
            marker_line_color = pero.colors.Blue,
            marker_fill_color = pero.colors.Blue.lighter(.2))
        
        legend2 = pero.MarkerLegend(
            text = "Second legend\nwith two lines",
            marker = "x",
            marker_line_color = pero.colors.Green,
            marker_fill_color = pero.colors.Green.lighter(.2))
        
        legend3 = pero.MarkerLegend(
            text = "Third legend",
            marker = "s",
            marker_line_color = pero.colors.Red,
            marker_fill_color = pero.colors.Red.lighter(.2))
        
        # init legend
        legend = pero.LegendBox(
            items = (legend1, legend2, legend3),
            orientation = pero.ORI_VERTICAL,
            fill_color = pero.colors.Ivory)
        
        # draw nw
        legend.draw(canvas,
            x = padding,
            y = padding,
            anchor = pero.POS_NW)
        
        # draw n
        legend.draw(canvas,
            x = 0.5*width,
            y = padding,
            anchor = pero.POS_N)
        
        # draw ne
        legend.draw(canvas,
            x = width-padding,
            y = padding,
            anchor = pero.POS_NE)
        
        # draw e
        legend.draw(canvas,
            x = width-padding,
            y = 0.5*height,
            anchor = pero.POS_E)
        
        # draw se
        legend.draw(canvas,
            x = width-padding,
            y = height-padding,
            anchor = pero.POS_SE)
        
        # draw s
        legend.draw(canvas,
            x = 0.5*width,
            y = height-padding,
            anchor = pero.POS_S)
        
        # draw sw
        legend.draw(canvas,
            x = padding,
            y = height-padding,
            anchor = pero.POS_SW)
        
        # draw w
        legend.draw(canvas,
            x = padding,
            y = 0.5*height,
            anchor = pero.POS_W)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'qt', "Legend", 500, 350)
