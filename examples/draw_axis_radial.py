#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for radial axis drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # init coords
        padding = 50
        width, height = canvas.viewport.wh
        radius = (min(width, height) - 2*padding)/2
        x = .5*width
        y = .5*height
        
        # init axis
        axis = pero.RadialAxis(
            
            units = pero.DEG,
            radius = radius,
            start_angle = pero.rads(0),
            end_angle = pero.rads(360),
            line_width = 2,
            
            labels = [str(i) for i in range(0, 360, 30)],
            label_rotation = pero.NATURAL,
            label_offset = 17,
            
            major_ticks = [i for i in range(0, 360, 30)],
            major_tick_size = 10,
            major_tick_offset = 1,
            major_tick_line_width = 2,
            
            minor_ticks = [i for i in range(0, 360, 6)],
            minor_tick_size = 6,
            minor_tick_offset = 5,
            minor_tick_line_color = "red")
        
        # draw outer axis
        axis.draw(canvas, x=x, y=y)
        
        # flip all
        axis.label_flip = True
        axis.major_tick_flip = True
        axis.minor_tick_flip = True
        
        # draw inner axis
        axis.draw(canvas, x=x, y=y, radius=0.75*radius)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Radial Axis", 400, 400)
