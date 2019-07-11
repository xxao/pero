#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for grid drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # set properties
        line_color = pero.colors.Blue
        
        # init glyphs
        origin = pero.Plus(
            size = 10,
            line_color = pero.colors.Red)
        
        label = pero.Text(
            text_align = pero.CENTER)
        
        # init coords
        x = 30
        y = 30
        
        # draw horizontal grid
        ticks = (0, 10, 20, 30, 40)
        grid = pero.ParallelGrid(ticks=ticks, length=40, angle=0, line_color=line_color, orientation=pero.HORIZONTAL)
        grid.draw(canvas, x=x, y=y)
        origin.draw(canvas, x=x, y=y)
        
        x += 80
        
        # draw horizontal grid (angled)
        grid = pero.ParallelGrid(ticks=ticks, length=40, angle=pero.rads(15), line_color=line_color, orientation=pero.HORIZONTAL)
        grid.draw(canvas, x=x, y=y)
        origin.draw(canvas, x=x, y=y)
        
        label.draw(canvas, x=x-40, y=y+70, text="ParallelGrid (H)")
        
        x += 80
        
        # draw vertical grid
        ticks = (0, 10, 20, 30, 40)
        grid = pero.ParallelGrid(ticks=ticks, length=40, angle=0, line_color=line_color, orientation=pero.VERTICAL)
        grid.draw(canvas, x=x, y=y)
        origin.draw(canvas, x=x, y=y)
        
        x += 90
        
        # draw vertical grid (angled)
        grid = pero.ParallelGrid(ticks=ticks, length=40, angle=pero.rads(15), line_color=line_color, orientation=pero.VERTICAL)
        grid.draw(canvas, x=x, y=y)
        origin.draw(canvas, x=x, y=y)
        
        label.draw(canvas, x=x-40, y=y+70, text="ParallelGrid (V)")
        
        x = 90
        y += 150
        
        # draw ray grid
        ticks = (0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330)
        grid = pero.RayGrid(ticks=ticks, length=25, offset=15, line_color=line_color, units=pero.DEG)
        grid.draw(canvas, x=x, y=y)
        origin.draw(canvas, x=x, y=y)
        label.draw(canvas, x=x, y=y+45, text="RayGrid")
        
        x += 150
        
        # draw radial grid
        ticks = (10, 20, 30, 40)
        grid = pero.RadialGrid(ticks=ticks, start_angle=pero.rads(-240), end_angle=pero.rads(60), line_color=line_color)
        grid.draw(canvas, x=x, y=y)
        origin.draw(canvas, x=x, y=y)
        label.draw(canvas, x=x, y=y+45, text="RadialGrid")


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Grid", 350, 270)
