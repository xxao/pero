#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for path rounding drawing."""
    
    
    def draw(self, canvas, *args, **kwargs):
        """Draws the test."""
        
        # clear canvas
        canvas.fill(pero.colors.White)
        
        # init path to round
        radius = 0.5 * min(canvas.width, canvas.height)
        star = pero.Path.make_star(
            rays = 10,
            x = 0.5 * canvas.width,
            y = 0.5 * canvas.height,
            outer_radius = 0.95 * radius,
            inner_radius = 0.35 * radius)
        
        # get anchors
        points = list(star.anchors())
        
        # init rounded shape
        rounded = pero.Path()
        rounded.move_to(*points[0])
        
        # prepare points for arc drawing
        points = points[1:] + points[:2]
        
        # add arcs
        control = points[0]
        for i, target in enumerate(points[1:]):
            rounded.arc_to(*control, *target, radius=10, before=i)
            control = target
        rounded.close()
        
        # draw original path
        canvas.line_color = "a"
        canvas.line_width = 1
        canvas.draw_path(star)
        
        # draw rounded path
        canvas.line_color = pero.colors.Blue.trans(0.5)
        canvas.line_width = 5
        canvas.draw_path(rounded)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Path Rounding", 400, 400)
