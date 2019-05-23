#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for path bbox calculation."""
    
    
    def draw(self, canvas, **overrides):
        """Draws the test."""
        
        # clear canvas
        canvas.line_scale = 1
        canvas.fill_color = pero.colors.White
        canvas.fill()
        
        # init glyphs
        pather = pero.Pather(
            show_handles = False)
        
        bbox = pero.Rect(
            line_color = pero.colors.Red,
            fill_color = None)
        
        # rect
        path = pero.Path().rect(50, 50, 100, 100)
        matrix = pero.Matrix().rotate(pero.rads(45), x=100, y=100)
        path.transform(matrix)
        pather.draw(canvas, path=path)
        
        box = path.bbox()
        bbox.draw(canvas, x=box.x, y=box.y, width=box.width, height=box.height)
        
        # circle
        path = pero.Path().circle(250, 100, 50)
        matrix = pero.Matrix().rotate(pero.rads(45), x=250, y=100)
        path.transform(matrix)
        pather.draw(canvas, path=path)
        
        box = path.bbox()
        bbox.draw(canvas, x=box.x, y=box.y, width=box.width, height=box.height)
        
        # path
        path = pero.Path() \
            .move_to(380, 50) \
            .curve_to(450, 50, 310, 150, 380, 150) \
            .curve_to(450, 150, 310, 50, 380, 50)
        
        matrix = pero.Matrix().rotate(pero.rads(45), x=380, y=100)
        path.transform(matrix)
        pather.draw(canvas, path=path)
        
        box = path.bbox()
        bbox.draw(canvas, x=box.x, y=box.y, width=box.width, height=box.height)


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Path Bounding Box", 450, 200)
