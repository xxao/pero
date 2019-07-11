#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for strait axis drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # init coords
        padding = 30
        offset = 50
        angles = list(map(pero.rads, (0, 45, 90, 135, 225, -45, -90, -180)))
        labels = ("0", "50", "100")
        splits = 5
        
        width, height = canvas.viewport.wh
        size = min(width/3, height/2)
        length = .5*size - padding - offset
        
        count = len(labels)-1
        major_ticks = [offset+i*length/count for i in range(count+1)]
        minor_ticks = [offset+i*length/(splits*count) for i in range(splits*count+1)]
        
        # init origin
        origin = pero.Cross(size=10, line_color=pero.colors.Red)
        
        # init axis
        axis = pero.StraitAxis(
            
            position = pero.RIGHT,
            relative = True,
            length = length,
            offset = offset,
            line_width = 2,
            
            labels = labels,
            label_offset = 12,
            
            title = "title",
            title_offset = 3,
            title_flip = True,
            
            major_ticks = major_ticks,
            major_tick_size = 7,
            major_tick_offset = 1,
            major_tick_line_width = 2,
            
            minor_ticks = minor_ticks,
            minor_tick_offset = 5,
            minor_tick_line_color = "red")
        
        # draw start title
        x = .5*size
        y = .5*size
        
        for angle in angles:
            axis.draw(canvas, x=x, y=y, angle=angle, title_position=pero.START)
            origin.draw(canvas, x=x, y=y)
        
        # draw middle title
        x += size
        
        for angle in angles:
            axis.draw(canvas, x=x, y=y, angle=angle, title_position=pero.MIDDLE)
            origin.draw(canvas, x=x, y=y)
        
        # draw end title
        x += size
        
        for angle in angles:
            axis.draw(canvas, x=x, y=y, angle=angle, title_position=pero.END)
            origin.draw(canvas, x=x, y=y)
        
        # flip all
        axis.title_flip = False
        axis.label_flip = True
        axis.major_tick_flip = True
        axis.minor_tick_flip = True
        
        # draw start title
        x = .5*size
        y += size
        
        for angle in angles:
            axis.draw(canvas, x=x, y=y, angle=angle, title_position=pero.START)
        
        # draw middle title
        x += size
        
        for angle in angles:
            axis.draw(canvas, x=x, y=y, angle=angle, title_position=pero.MIDDLE)
        
        # draw end title
        x += size
        
        for angle in angles:
            axis.draw(canvas, x=x, y=y, angle=angle, title_position=pero.END)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Strait Axis", 800, 550)
