#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for path arc drawing."""
    
    
    def draw_test(self, canvas, c, p1, p2, radius, angle=0, before=True, after=False, limit=False):
        """Draws the test."""
        
        # get coords
        p1x, p1y = p1
        p2x, p2y = p2
        cx, cy = c
        
        # apply angle
        if angle:
            matrix = pero.Matrix().rotate(pero.rads(angle), cx, cy)
            p1x, p1y = matrix.transform(p1x, p1y)
            p2x, p2y = matrix.transform(p2x, p2y)
        
        # make path
        path = pero.Path()
        path.move_to(p1x, p1y)
        path.arc_to(cx, cy, p2x, p2y, radius,
            before = before,
            after = after,
            limit = limit)
        
        # make pather glyph
        pather = pero.Pather(
            path = path,
            line_width = 13,
            line_cap = pero.LINE_CAP_ROUND,
            line_color = pero.colors.LightBlue,
            line_alpha = 230,
            fill_color = None,
            anchor_fill_color = pero.colors.Blue,
            show_handles = False)
        
        # draw guides
        canvas.line_width = 1
        canvas.line_color = "black"
        canvas.fill_color = None
        canvas.draw_line(p1x, p1y, cx, cy)
        canvas.draw_line(p2x, p2y, cx, cy)
        
        # draw start point
        canvas.line_width = 1
        canvas.line_color = "black"
        canvas.fill_color = "black"
        canvas.draw_circle(p1x, p1y, 5)
        
        # draw end point
        canvas.line_width = 1
        canvas.line_color = "black"     
        canvas.fill_color = "lightgrey"
        canvas.draw_circle(p2x, p2y, 4)
        
        # draw control point
        canvas.line_width = 0
        canvas.line_color = None
        canvas.fill_color = "red"
        canvas.draw_circle(cx, cy, 3)
        
        # draw path        
        pather.draw(canvas)
    
    
    def draw(self, canvas, *args, **kwargs):
        """Draws the test."""
        
        # clear canvas
        canvas.fill(pero.colors.White)
        
        # set coords
        angle = -10
        radius = 15
        before = False
        after = False
        limit = True
        
        # left
        canvas.view(100, 100)
        self.draw_test(canvas, (0, 0), (-50, 0), (-50, 50), radius, angle, before, after, limit)
        
        canvas.view(100, relative=True)
        self.draw_test(canvas, (0, 0), (-50, 0), (0, 50), radius, angle, before, after, limit)
        
        canvas.view(100, relative=True)
        self.draw_test(canvas, (0, 0), (-50, 0), (50, 50), radius, angle, before, after, limit)
        
        canvas.view(100, relative=True)
        self.draw_test(canvas, (0, 0), (-50, 0), (50, 0), radius, angle, before, after, limit)
        
        canvas.view(150, relative=True)
        self.draw_test(canvas, (0, 0), (-50, 0), (50, -50), radius, angle, before, after, limit)
        
        canvas.view(100, relative=True)
        self.draw_test(canvas, (0, 0), (-50, 0), (0, -50), radius, angle, before, after, limit)
        
        canvas.view(100, relative=True)
        self.draw_test(canvas, (0, 0), (-50, 0), (-50, -50), radius, angle, before, after, limit)
        
        # left reversed
        canvas.view(100, 200)
        self.draw_test(canvas, (0, 0), (-50, 50), (-50, 0), radius, angle, before, after, limit)
        
        canvas.view(100, relative=True)
        self.draw_test(canvas, (0, 0), (0, 50), (-50, 0), radius, angle, before, after, limit)
        
        canvas.view(100, relative=True)
        self.draw_test(canvas, (0, 0), (50, 50), (-50, 0), radius, angle, before, after, limit)
        
        canvas.view(100, relative=True)
        self.draw_test(canvas, (0, 0), (50, 0), (-50, 0), radius, angle, before, after, limit)
        
        canvas.view(150, relative=True)
        self.draw_test(canvas, (0, 0), (50, -50), (-50, 0), radius, angle, before, after, limit)
        
        canvas.view(100, relative=True)
        self.draw_test(canvas, (0, 0), (0, -50), (-50, 0), radius, angle, before, after, limit)
        
        canvas.view(100, relative=True)
        self.draw_test(canvas, (0, 0), (-50, -50), (-50, 0), radius, angle, before, after, limit)
        
        # right
        canvas.view(50, 350)
        self.draw_test(canvas, (0, 0), (50, 0), (50, 50), radius, angle, before, after, limit)
        
        canvas.view(100, relative=True)
        self.draw_test(canvas, (0, 0), (50, 0), (0, 50), radius, angle, before, after, limit)
        
        canvas.view(100, relative=True)
        self.draw_test(canvas, (0, 0), (50, 0), (-50, 50), radius, angle, before, after, limit)
        
        canvas.view(150, relative=True)
        self.draw_test(canvas, (0, 0), (50, 0), (-50, 0), radius, angle, before, after, limit)
        
        canvas.view(100, relative=True)
        self.draw_test(canvas, (0, 0), (50, 0), (-50, -50), radius, angle, before, after, limit)
        
        canvas.view(100, relative=True)
        self.draw_test(canvas, (0, 0), (50, 0), (0, -50), radius, angle, before, after, limit)
        
        canvas.view(100, relative=True)
        self.draw_test(canvas, (0, 0), (50, 0), (50, -50), radius, angle, before, after, limit)
        
        # right reversed
        canvas.view(50, 450)
        self.draw_test(canvas, (0, 0), (50, 50), (50, 0), radius, angle, before, after, limit)
        
        canvas.view(100, relative=True)
        self.draw_test(canvas, (0, 0), (0, 50), (50, 0), radius, angle, before, after, limit)
        
        canvas.view(100, relative=True)
        self.draw_test(canvas, (0, 0), (-50, 50), (50, 0), radius, angle, before, after, limit)
        
        canvas.view(150, relative=True)
        self.draw_test(canvas, (0, 0), (-50, 0), (50, 0), radius, angle, before, after, limit)
        
        canvas.view(100, relative=True)
        self.draw_test(canvas, (0, 0), (-50, -50), (50, 0), radius, angle, before, after, limit)
        
        canvas.view(100, relative=True)
        self.draw_test(canvas, (0, 0), (0, -50), (50, 0), radius, angle, before, after, limit)
        
        canvas.view(100, relative=True)
        self.draw_test(canvas, (0, 0), (50, -50), (50, 0), radius, angle, before, after, limit)
        
        # overlaps
        canvas.view(50, 600)
        self.draw_test(canvas, (0, 0), (50, 50), (50, 50), radius, angle, before, after, limit)
        
        canvas.view(50, relative=True)
        self.draw_test(canvas, (0, 0), (0, 0), (50, 0), radius, angle, before, after, limit)
        
        canvas.view(70, relative=True)
        self.draw_test(canvas, (0, 0), (50, 50), (0, 0), radius, angle, before, after, limit)
        
        # no radius
        canvas.view(150, relative=True)
        self.draw_test(canvas, (0, 0), (-50, 0), (-50, 50), None, angle, before, after, limit)
        
        canvas.view(100, relative=True)
        self.draw_test(canvas, (0, 0), (-50, 0), (-50, 50), 0, angle, before, after, limit)
        
        # over limit
        canvas.view(150, relative=True)
        self.draw_test(canvas, (0, 0), (-50, 0), (-50, 50), 50, angle, before, after, limit)
        
        canvas.view(50, relative=True)
        self.draw_test(canvas, (0, 0), (50, 0), (50, 50), 50, angle, before, after, limit)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Path ArcTo", 800, 750)
