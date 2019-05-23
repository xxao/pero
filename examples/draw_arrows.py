#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import math
import pero


class DrawTest(pero.Graphics):
    """Test case for arrows drawing."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # set properties
        arrow_size = 15
        line_width = 1
        line_color = pero.colors.Blue
        start_fill_color = pero.colors.Red.opaque(0.25)
        end_fill_color = pero.colors.Blue.opaque(0.25)
        
        # init glyphs
        label = pero.Text(
            text_align = pero.CENTER)
        
        start_head = pero.NormalHead(
            size = arrow_size,
            line_color = line_color,
            fill_color = start_fill_color)
        
        end_head = pero.NormalHead(
            size = arrow_size,
            line_color = line_color,
            fill_color = end_fill_color)
        
        # init coords
        x = 70
        y1 = 40
        y2 = 140
        
        # draw guides
        canvas.line_color = pero.colors.Red
        canvas.draw_line(20, y1, 680, y1)
        canvas.draw_line(20, y2, 680, y2)
        
        # test line arrow
        arrow = pero.LineArrow(start_head=start_head, end_head=end_head, line_width=line_width, line_color=line_color)
        arrow.draw(canvas, x1=x-25, y1=y1, x2=x+25, y2=y2)
        label.draw(canvas, x=x, y=y2+20, text="LineArrow")
        
        x += 100
        
        # test ray arrow
        arrow = pero.RayArrow(start_head=start_head, end_head=end_head, line_width=line_width, line_color=line_color)
        arrow.draw(canvas, x=x-25, y=y1, angle=math.radians(80), length=100)
        label.draw(canvas, x=x, y=y2+20, text="RayArrow")
        
        x += 100
        
        # test arc arrow
        arrow = pero.ArcArrow(start_head=start_head, end_head=end_head, line_width=line_width, line_color=line_color)
        arrow.draw(canvas, x=x, y=0.5*(y1+y2), start_angle=math.radians(-160), end_angle=math.radians(40), radius=50, clockwise=True)
        label.draw(canvas, x=x, y=y2+20, text="ArcArrow")
        
        x += 120
        
        # test bow arrow
        arrow = pero.BowArrow(start_head=start_head, end_head=end_head, line_width=line_width, line_color=line_color)
        arrow.draw(canvas, x1=x-30, y1=y1, x2=x+30, y2=y2, radius=100, large=False, clockwise=True)
        label.draw(canvas, x=x, y=y2+20, text="BowArrow")
        
        x += 100
        
        # test curve arrow
        arrow = pero.CurveArrow(start_head=start_head, end_head=end_head, line_width=line_width, line_color=line_color)
        arrow.draw(canvas, x1=x-25, y1=y1, x2=x+25, y2=y2)
        label.draw(canvas, x=x, y=y2+20, text="CurveArrow")
        
        x += 100
        
        # test path arrow
        path = pero.Path().move_to(10,10).line_to(25,10).line_to(30, 15).line_to(40,5).line_to(45,10).line_to(60,10)
        arrow = pero.PathArrow(start_head=start_head, end_head=end_head, line_width=line_width, line_color=line_color)
        arrow.draw(canvas, x1=x-25, y1=y1, x2=x+25, y2=y2, path=path)
        label.draw(canvas, x=x, y=y2+20, text="PathArrow")
        
        x = 70
        y1 += 200
        y2 += 200
        
        # draw guides
        canvas.line_color = pero.colors.Red
        canvas.draw_line(20, y1, 680, y1)
        canvas.draw_line(20, y2, 680, y2)
        
        # init sample arrow
        arrow = pero.LineArrow(line_width=line_width, line_color=line_color)
        
        # test no heads
        arrow.draw(canvas, x1=x-25, y1=y1, x2=x+25, y2=y2)
        label.draw(canvas, x=x, y=y2+20, text="No Heads")
        
        x += 90
        
        # test line heads
        arrow.start_head = pero.LineHead(size=arrow_size, line_color=line_color, fill_color=start_fill_color)
        arrow.end_head = pero.LineHead(size=arrow_size, line_color=line_color, fill_color=end_fill_color)
        arrow.draw(canvas, x1=x-25, y1=y1, x2=x+25, y2=y2)
        label.draw(canvas, x=x, y=y2+20, text="LineHead")
        
        x += 90
        
        # test normal heads
        arrow.start_head = pero.NormalHead(size=arrow_size, line_color=line_color, fill_color=start_fill_color)
        arrow.end_head = pero.NormalHead(size=arrow_size, line_color=line_color, fill_color=end_fill_color)
        arrow.draw(canvas, x1=x-25, y1=y1, x2=x+25, y2=y2)
        label.draw(canvas, x=x, y=y2+20, text="NormalHead")
        
        x += 90
        
        # test open heads
        arrow.start_head = pero.OpenHead(size=arrow_size, line_color=line_color, fill_color=start_fill_color)
        arrow.end_head = pero.OpenHead(size=arrow_size, line_color=line_color, fill_color=end_fill_color)
        arrow.draw(canvas, x1=x-25, y1=y1, x2=x+25, y2=y2)
        label.draw(canvas, x=x, y=y2+20, text="OpenHead")
        
        x += 90
        
        # test V heads
        arrow.start_head = pero.VeeHead(size=arrow_size, line_color=line_color, fill_color=start_fill_color)
        arrow.end_head = pero.VeeHead(size=arrow_size, line_color=line_color, fill_color=end_fill_color)
        arrow.draw(canvas, x1=x-25, y1=y1, x2=x+25, y2=y2)
        label.draw(canvas, x=x, y=y2+20, text="VeeHead")
        
        x += 90
        
        # test circle heads
        arrow.start_head = pero.CircleHead(size=arrow_size, line_color=line_color, fill_color=start_fill_color)
        arrow.end_head = pero.CircleHead(size=arrow_size, line_color=line_color, fill_color=end_fill_color)
        arrow.draw(canvas, x1=x-25, y1=y1, x2=x+25, y2=y2)
        label.draw(canvas, x=x, y=y2+20, text="CircleHead")
        
        x += 90
        
        # test symbol heads
        path = pero.Path.make_ngon(5).transformed(pero.Matrix().rotate(pero.rads(90)))
        arrow.start_head = pero.SymbolHead(path=path, size=arrow_size, line_color=line_color, fill_color=start_fill_color)
        arrow.end_head = pero.SymbolHead(path=path, size=arrow_size, line_color=line_color, fill_color=end_fill_color)
        arrow.draw(canvas, x1=x-25, y1=y1, x2=x+25, y2=y2)
        label.draw(canvas, x=x, y=y2+20, text="SymbolHead")


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Arrows", 700, 400)
