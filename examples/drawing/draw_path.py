#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

import pero


class DrawTest(pero.Graphics):
    """Test case for path drawing."""
    
    
    def draw(self, canvas, *args, **kwargs):
        """Draws the test."""
        
        # clear canvas
        canvas.fill(pero.colors.White)
        
        # init path
        path = pero.Path()
        
        # init glyph
        glyph = pero.Pather()
        
        # init label
        label = pero.Text()
        
        # init transformation matrix
        matrix = pero.Matrix()
        
        # init coords
        x = 25
        y = 25
        matrix.clear().translate(x, y)
        
        # add move to
        path.move_to(10, 20, relative=True)
        glyph.draw(canvas, path=path.transformed(matrix))
        label.draw(canvas, x=x, y=y+80, text="MoveTo")
        
        x += 80
        matrix.clear().translate(x, y)
        
        # add line to
        path.line_to(25, 50, relative=True)
        glyph.draw(canvas, path=path.transformed(matrix))
        label.draw(canvas, x=x, y=y+80, text="LineTo")
        
        x += 100
        matrix.clear().translate(x, y)
        
        # add curve to
        path.curve_to(25, 0, 25, -30, 15, -50, relative=True)
        glyph.draw(canvas, path=path.transformed(matrix))
        label.draw(canvas, x=x, y=y+80, text="CurveTo")
        
        x += 100
        matrix.clear().translate(x, y)
        
        # add smooth to
        path.curve_s_to(25, -30, 25, 0, relative=True)
        glyph.draw(canvas, path=path.transformed(matrix))
        label.draw(canvas, x=x, y=y+80, text="SmoothTo")
        
        x += 120
        matrix.clear().translate(x, y)
        
        # add move to
        path.move_to(0, 30, relative=True)
        glyph.draw(canvas, path=path.transformed(matrix))
        label.draw(canvas, x=x, y=y+80, text="MoveTo")
        
        x += 120
        matrix.clear().translate(x, y)
        
        # add line to
        path.line_to(25, 25, relative=True)
        glyph.draw(canvas, path=path.transformed(matrix))
        label.draw(canvas, x=x, y=y+80, text="LineTo")
        
        x += 130
        matrix.clear().translate(x, y)
        
        # add smooth to
        path.curve_s_to(25, 0, 25, -25, relative=True)
        glyph.draw(canvas, path=path.transformed(matrix))
        label.draw(canvas, x=x, y=y+80, text="SmoothTo")
        
        x = 25
        y += 150
        matrix.clear().translate(x, y)
        glyph.show_anchors = False
        glyph.show_handles = False
        
        # add circle
        path.circle(0, -30, 20, relative=True)
        glyph.draw(canvas, path=path.transformed(matrix))
        label.draw(canvas, x=x, y=y+80, text="Circle")
        
        x += 200
        matrix.clear().translate(x, y)
        
        # add ellipse
        path.ellipse(0, 0, 30, 15, relative=True)
        glyph.draw(canvas, path=path.transformed(matrix))
        label.draw(canvas, x=x, y=y+80, text="Ellipse")
        
        x += 200
        matrix.clear().translate(x, y)
        
        # add rectangle
        path.rect(170, 10, 30, 50)
        glyph.draw(canvas, path=path.transformed(matrix))
        label.draw(canvas, x=x, y=y+80, text="Rectangle")
        
        x += 250
        matrix.clear().translate(x, y)
        
        # add rounded rectangle
        path.rect(-10, -10, 50, 70, 10, relative=True)
        glyph.draw(canvas, path=path.transformed(matrix))
        label.draw(canvas, x=x, y=y+80, text="Round Rectangle")
        
        x = 25
        y += 150
        matrix.clear().translate(x, y)
        
        # add polygon
        points = pero.make_star(6, x=265, y=35, outer_radius=40, inner_radius=20).anchors()
        path.polygon(points)
        glyph.draw(canvas, path=path.transformed(matrix))
        label.draw(canvas, x=x, y=y+80, text="Polygon")
        
        x += 350
        matrix.clear().translate(x, y)
        
        # split path
        glyph.show_anchors = False
        glyph.show_handles = False
        glyph.fill_color = None
        glyph.line_color = lambda d: pero.colors.Pero[d]
        glyph.line_width = 2
        
        for i, subpath in enumerate(path.transformed(matrix).split()):
            glyph.draw(canvas, i, path=subpath)
        
        label.draw(canvas, x=x, y=y+80, text="Split")


# run test
if __name__ == '__main__':
    pero.debug(DrawTest(), 'show', "Path Drawing", 950, 450)
