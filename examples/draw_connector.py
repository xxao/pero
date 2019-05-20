#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for connector arrows drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # set properties
        arrow_size = 15
        line_color = pero.colors.Blue
        start_fill_color = pero.colors.Red.opaque(0.25)
        end_fill_color = pero.colors.Blue.opaque(0.25)
        
        # init arrow
        arrow = pero.ConnectorArrow(line_color=line_color)
        arrow.start_head = pero.NormalHead(size=arrow_size, line_color=line_color, fill_color=start_fill_color)
        arrow.end_head = pero.NormalHead(size=arrow_size, line_color=line_color, fill_color=end_fill_color)
        
        # init coords
        x = 50
        y1 = 40
        y2 = 140
        
        # draw guides
        canvas.line_color = pero.colors.Red
        canvas.draw_line(20, y1, 660, y1)
        canvas.draw_line(20, y2, 660, y2)
        
        # test horizontal connector arrow
        arrow.draw(canvas, x1=x-25, y1=y1, x2=x+25, y2=y2, orientation=pero.HORIZONTAL)
        x += 70
        arrow.draw(canvas, x1=x+25, y1=y1, x2=x-25, y2=y2, orientation=pero.HORIZONTAL)
        
        # test vertical connector arrow
        x += 100
        arrow.draw(canvas, x1=x-25, y1=y1, x2=x+25, y2=y2, orientation=pero.VERTICAL)
        x += 70
        arrow.draw(canvas, x1=x+25, y1=y1, x2=x-25, y2=y2, orientation=pero.VERTICAL)
        
        # test horizontal curved connector arrow
        x += 100
        arrow.draw(canvas, x1=x-30, y1=y1, x2=x+30, y2=y2, curve=1, orientation=pero.HORIZONTAL)
        x += 70
        arrow.draw(canvas, x1=x+30, y1=y1, x2=x-30, y2=y2, curve=1, orientation=pero.HORIZONTAL)
        
        # test vertical curved connector arrow
        x += 100
        arrow.draw(canvas, x1=x-25, y1=y1, x2=x+25, y2=y2, curve=1, orientation=pero.VERTICAL)
        x += 70
        arrow.draw(canvas, x1=x+25, y1=y1, x2=x-25, y2=y2, curve=1, orientation=pero.VERTICAL)
        
        x = 50
        y1 += 150
        y2 += 150
        
        # draw guides
        canvas.line_color = pero.colors.Red
        canvas.draw_line(20, y1, 660, y1)
        canvas.draw_line(20, y2, 660, y2)
        
        # test horizontal connector arrow
        arrow.draw(canvas, x1=x-20, y1=y1, x2=x+20, y2=y2, pivot=0, orientation=pero.HORIZONTAL)
        x += 20
        arrow.draw(canvas, x1=x-20, y1=y1, x2=x+20, y2=y2, pivot=1, orientation=pero.HORIZONTAL)
        
        # test vertical connector arrow
        x += 100
        arrow.draw(canvas, x1=x-20, y1=y1, x2=x+20, y2=y2, pivot=0, orientation=pero.VERTICAL)
        x += 70
        arrow.draw(canvas, x1=x-20, y1=y1, x2=x+20, y2=y2, pivot=1, orientation=pero.VERTICAL)
        
        # test horizontal curved connector arrow
        x += 100
        arrow.draw(canvas, x1=x-40, y1=y1, x2=x+40, y2=y2, pivot=0, curve=1, orientation=pero.HORIZONTAL)
        x += 20
        arrow.draw(canvas, x1=x-40, y1=y1, x2=x+40, y2=y2, pivot=1, curve=1, orientation=pero.HORIZONTAL)
        
        # test vertical curved connector arrow
        x += 100
        arrow.draw(canvas, x1=x-40, y1=y1, x2=x+40, y2=y2, pivot=0, curve=1, orientation=pero.VERTICAL)
        x += 70
        arrow.draw(canvas, x1=x-40, y1=y1, x2=x+40, y2=y2, pivot=1, curve=1, orientation=pero.VERTICAL)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Connector Arrows", 680, 330)
